import os
from torchvision import transforms
from PIL import Image
import numpy as np
import torch
import cv2
import base64

from .net import DeepRank
from .apps import ApiConfig


# ---------------------------
# pre-processing component
data_transforms = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
# ---------------------------

# ---------------------------
# config file path info
MARK_MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets/mark.pt')
DESIGN_MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets/design.pt')
MARK_NUMBERS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets/mark_numbers.txt')
DESIGN_NUMBERS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets/design_numbers.txt')
MARK_EMBEDDING_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets/mark_embedding.txt')
DESIGN_EMBEDDING_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets/design_embedding.txt')
WEIGHT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets/yolov3.weights')
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets/yolov3.cfg')
# ---------------------------


def euclidean_distance(x, y):
    """
    calculate euclidean distance

    :param x: feature map x
    :param y: feature map y
    :return: l2 distance between x and y
    """
    return np.sqrt(np.sum(x - y, axis=1) ** 2)


def query_embedding(model, query_image_path, detected):
    """
    단일 요청 이미지에 대해 feature map 을 생성한다.

    :param model: deep ranking model
    :param query_image_path: request image path
    :param detected: processed object detection
    :return: feature map
    """
    # read query image and pre-processing
    if detected:
        query_image = Image.fromarray(query_image_path, 'RGB')
    else:
        query_image = Image.open(query_image_path).convert('RGB')

    query_image = data_transforms(query_image)
    query_image = query_image[None]  # add new axis

    model.eval()  # set to eval mode

    embedding = model(query_image)

    return embedding.cpu().detach().numpy()


def predict(query_image, result_num, image_type, detected=False):
    """
    요청 이미지를 통해 가장 유사한 이미지들을 찾는다.

    :param query_image: requested image (base64)
    :param result_num: requested number
    :param image_type: mark or design image
    :param detected: processed object-detection
    :return: similar images
    """

    model = DeepRank()

    # 디자인과 상표 이미지 분리해서 트리플렛 및 임베딩 파일 관리
    if image_type == 0:
        ''' 상표 이미지 '''
        model.load_state_dict(torch.load(MARK_MODEL_PATH, map_location=torch.device('cpu')))
        query_embedded = query_embedding(model, query_image, detected)
        train_embedded = np.fromfile(MARK_EMBEDDING_PATH, dtype=np.float32).reshape(-1, 4096)
        f = open(MARK_NUMBERS_PATH, 'r')
    else:
        ''' 디자인 이미지 '''
        model.load_state_dict(torch.load(DESIGN_MODEL_PATH, map_location=torch.device('cpu')))
        query_embedded = query_embedding(model, query_image, detected)
        train_embedded = np.fromfile(DESIGN_EMBEDDING_PATH, dtype=np.float32).reshape(-1, 4096)
        f = open(DESIGN_NUMBERS_PATH, 'r')

    app_nums = f.readlines()
    app_nums = list(map(lambda s: s.strip(), app_nums))

    #  by euclidean distance, find top ranked similar images
    image_dist = euclidean_distance(train_embedded, query_embedded)
    image_dist_indexed = zip(image_dist, range(image_dist.shape[0]))
    image_dist_sorted = sorted(image_dist_indexed, key=lambda x: x[0])

    # top related images
    predicted_images = [(img[0], app_nums[img[1]]) for img in image_dist_sorted[:result_num]]

    return predicted_images


# object detection 대상 클래스 레이블
classes = ['chicken', 'pig']


def object_detection(query_image):
    """
    요청 이미지에서 객체를 검출한 결과를 생성한다.

    :param query_image: requested image (base64)
    :return: detection result image (base64)
    """
    # load model
    net = cv2.dnn.readNet(WEIGHT_PATH, CONFIG_PATH)
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # input image preprocess
    pil_img = Image.open(query_image)
    img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    img = cv2.resize(img, None, fx=0.4, fy=0.4)
    blob_img = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), swapRB=True, crop=False)

    # forward
    net.setInput(blob_img)
    outs = net.forward(output_layers)

    # handle result
    class_indices = []
    confidences = []
    boxes = []
    (H, W) = img.shape[:2]
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_idx = np.argmax(scores)
            confidence = scores[class_idx]
            if confidence > 0.5:
                center_x = int(detection[0] * W)
                center_y = int(detection[1] * H)
                w = int(detection[2] * W)
                h = int(detection[3] * H)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_indices.append(class_idx)

    # 한 객체에 대해 중복되는 박스들을 지운다
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # case 1: 객체가 하나도 발견되지 않을 경우
    if len(indexes) == 0:
        print('query image detected: nothing')
        return query_image, False

    # case 2, 3: 하나이상 발견될 경우
    for i in range(len(boxes)):
        if i in indexes:
            (x, y, w, h) = boxes[i]
            src = img.copy()
            crop_img = src[y:y + h, x:x + w]
            label = classes[class_indices[i]]
            print('query image detected: ' + label)
            return crop_img, True

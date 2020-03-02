import os
from torchvision import transforms
from PIL import Image
from collections import OrderedDict
import pandas as pd
import numpy as np
import torch

from .net import DeepRank

# -- pre-processing component
data_transforms = transforms.Compose([
        transforms.Resize((224, 224), interpolation=2),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])


def euclidean_distance(x, y):
    """ calculate euclidean distance """
    return np.sqrt(np.sum(x - y, axis=1) ** 2)


# -- path info
TRIPLET_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'triplet.csv')
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'deeprank.pt')
EMBEDDING_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'embedding.txt')


def query_embedding(model, query_image_path):
    # read query image and pre-processing
    query_image = Image.open(query_image_path).convert('RGB')
    query_image = data_transforms(query_image)
    query_image = query_image[None]  # add new axis

    model.eval()  # set to eval mode

    embedding = model(query_image)

    return embedding.cpu().detach().numpy()


def predict(query_image, result_num):
    model = DeepRank()
    model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))  # load model parameters

    train_df = pd.read_csv(TRIPLET_PATH)
    train_embedded = np.fromfile(EMBEDDING_PATH, dtype=np.float32).reshape(-1, 4096)

    # embedding query image
    query_embedded = query_embedding(model, query_image)

    #  by euclidean distance, find top ranked similar images
    image_dist = euclidean_distance(train_embedded, query_embedded)
    image_dist_indexed = zip(image_dist, range(image_dist.shape[0]))
    image_dist_sorted = sorted(image_dist_indexed, key=lambda x: x[0])

    # top 5 images
    predicted_images = [(img[0], train_df.loc[img[1], "query"]) for img in image_dist_sorted[:result_num]]

    return predicted_images


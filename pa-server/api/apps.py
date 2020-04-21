from django.apps import AppConfig
from io import BytesIO
from .net import DeepRank
import boto3
import torch
from django.conf import settings


s3_target_list = {
    'mark_model': 'model/deeprank.pt',
    'mark_triplet': 'triplet/triplet.csv',
    'mark_embedding': 'embedding/embedding.txt',
    'design_model': 'model/deeprank.pt',
    'design_triplet': 'triplet/triplet.csv',
    'design_embedding': 'embedding/embedding.txt',
    'yolo_cfg': 'yolo/yolov3.cfg',
    'yolo_weights': 'yolo/yolov3.weights',
}


class ApiConfig(AppConfig):
    """
    api 앱 설정을 변경한다.

    core 는 외부에 공개되는 변수
    """
    name = 'api'
    core = {
        'mark_model': DeepRank(),
        'design_model': DeepRank(),
    }

    def ready(self):
        """
        앱 초기화시 필요한 작업들을 수행한다.

        :return: None
        """
        # create s3 client
        s3client = boto3.client('s3',
                                aws_access_key_id=settings.S3_ACCESS_KEY,
                                aws_secret_access_key=settings.S3_SECRET_KEY)

        # get objects from s3 /w hints
        response = {}
        for key, path in s3_target_list.items():
            response[key] = s3client.get_object(Bucket='patentattorney-bucket', Key=path)
        print('load all necessary files from s3')

        # read data from s3
        for target, data in response.items():
            body = response[target]['Body'].read()

            if target.endswith('model'):
                stream = BytesIO(body)
                ApiConfig.core[target].load_state_dict(torch.load(stream))  # load parameter data
            elif target.endswith('triplet'):
                stream = BytesIO(body)
                ApiConfig.core[target] = stream
            else:
                ApiConfig.core[target] = body

            print(f'read {target} data from s3')

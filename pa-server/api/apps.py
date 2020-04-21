from django.apps import AppConfig
from io import BytesIO
from .net import DeepRank
import boto3
import torch
from django.conf import settings


class ApiConfig(AppConfig):
    name = 'api'
    stream = None
    model = DeepRank()

    def ready(self):
        # create s3 client
        s3client = boto3.client('s3',
                                aws_access_key_id=settings.S3_ACCESS_KEY,
                                aws_secret_access_key=settings.S3_SECRET_KEY)

        # get object from s3 /w hints
        response = s3client.get_object(Bucket='patentattorney-bucket', Key='model/deeprank.pt')

        # read data from s3
        body = response['Body'].read()
        ApiConfig.stream = BytesIO(body)
        ApiConfig.model.load_state_dict(torch.load(ApiConfig.stream))  # load model
        print('read deeprank.pt from s3')

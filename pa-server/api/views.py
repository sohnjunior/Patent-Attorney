from django.views.generic import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .ai.utils import predict

import base64
from io import BytesIO
from PIL import Image
import json
import os

from .utils import request_open_api, base64_encoder, parse_application_number

STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')


@method_decorator(csrf_exempt, name='dispatch')
class MarkInfo(View):
    """
    상표 출원번호를 기준으로 등록된 특허 정보 반환
    """
    def get(self, request, *args, **kwargs):
        query_app_num = request.GET['appnum']  # query application number
        parsed_data = request_open_api(application_number=query_app_num, mode=0)

        return JsonResponse(data=json.dumps(parsed_data), status=200, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class DesignInfo(View):
    """
    디자인 출원번호를 기준으로 등록된 디자인 정보 반환
    """
    def get(self, request, *args, **kwargs):
        query_app_num = request.GET['appnum']  # query application number
        print(query_app_num)
        parsed_data = request_open_api(application_number=query_app_num, mode=1)

        return JsonResponse(data=json.dumps(parsed_data), status=200, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class PatentPredict(View):
    """
    특허청에 등록된 이미지들을 기반으로 유사도 분석 결과 반환
    """
    def post(self, request, *args, **kwargs):
        search_type = int(request.POST['searchType'])  # 요청 타입 (0: 상표 1: 디자인)
        request_num = int(request.POST['selected'])  # 요청한 유사 이미지 개수
        query_image = request.FILES['file']  # 요청 이미지

        # deep ranking TODO search type 에 따라 object detection 수행
        result = predict(query_image, request_num)

        # static folder 에 이미지 데이터 구성해놓고 결과 이미지 로드해서 반환해주기
        app_nums = []
        img_binary = []
        for info in result:
            img_path = os.path.join(STATIC_PATH, info[1])

            # info[1] format: patent_image/train/닭/4020020037823.jpg
            app_num = parse_application_number(info[1])
            app_nums.append(app_num)

            # gray scale 로 읽히는 이미지들이 있어서 RGB 형식으로 바꿔줌
            raw_image = Image.open(img_path).convert('RGB')

            # convert PIL image to base64 string
            img_str = base64_encoder(raw_image)
            img_binary.append(img_str)

        # encoding request image to base64
        raw_image = Image.open(query_image).convert('RGB')
        query_image_base64 = base64_encoder(raw_image)

        # response object
        res = {
            "request_num": request_num,
            "request_image": query_image_base64,
            "images": img_binary,
            "result_app_numbers": app_nums
        }

        return JsonResponse(data=json.dumps(res), status=200, safe=False)





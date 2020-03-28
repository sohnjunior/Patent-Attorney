from django.views.generic import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict

from .ai.utils import predict, object_detection

import base64
from io import BytesIO
from PIL import Image
from urllib.request import urlopen
import json

from .models import MarkPatentInfo, DesignPatentInfo
from .utils import base64_encoder, parse_application_number


@method_decorator(csrf_exempt, name='dispatch')
class MarkInfo(View):
    """
    상표 출원번호를 기준으로 등록된 특허 정보 반환
    """
    def get(self, request, *args, **kwargs):
        query_app_num = str(self.kwargs.get('pk'))  # query application number
        obj = MarkPatentInfo.objects.get(app_num=query_app_num)
        data = model_to_dict(obj)

        return JsonResponse(data=json.dumps(data), status=200, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class DesignInfo(View):
    """
    디자인 출원번호를 기준으로 등록된 디자인 정보 반환
    """
    def get(self, request, *args, **kwargs):
        query_app_num = str(self.kwargs.get('pk'))  # query application number
        obj = DesignPatentInfo.objects.get(app_num=query_app_num)
        data = model_to_dict(obj)

        return JsonResponse(data=json.dumps(data), status=200, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class PatentPredict(View):
    """
    특허청에 등록된 이미지들을 기반으로 유사도 분석 결과 반환
    """
    def post(self, request, *args, **kwargs):
        search_type = int(request.POST['searchType'])  # 요청 타입 (0: 상표 1: 디자인)
        request_num = int(request.POST['selected'])  # 요청한 유사 이미지 개수
        query_image = request.FILES['file']  # 요청 이미지

        # deep ranking
        # search type 에 따라 object detection 수행
        detected = False
        if search_type == 0:
            query_image, detected = object_detection(query_image=query_image)
        result = predict(query_image, request_num, detected)

        app_nums = []
        img_binary = []
        for info in result:
            # info[1] format: patent_image/train/닭/4020020037823.jpg
            app_num = parse_application_number(info[1])
            app_nums.append(app_num)

            # gray scale 로 읽히는 이미지들이 있어서 RGB 형식으로 바꿔줌
            try:
                if search_type == 0:
                    obj = MarkPatentInfo.objects.get(app_num=app_num)
                else:
                    obj = DesignPatentInfo.objects.get(app_num=app_num)
                url = obj.image_path
                raw_image = Image.open(urlopen(url)).convert('RGB')

                # convert PIL image to base64 string
                img_str = base64_encoder(raw_image)
                img_binary.append(img_str)
            except ObjectDoesNotExist:
                print('해당 출원번호에 해당하는 정보가 존재하지 않습니다.')

        # encoding request image to base64
        raw_image = Image.open(request.FILES['file']).convert('RGB')
        query_image_base64 = base64_encoder(raw_image)

        # response object
        res = {
            "request_num": request_num,
            "request_image": query_image_base64,
            "images": img_binary,
            "result_app_numbers": app_nums
        }

        return JsonResponse(data=json.dumps(res), status=200, safe=False)





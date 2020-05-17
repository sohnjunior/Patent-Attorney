from django.views.generic import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

from .research import predict, object_detection

from PIL import Image
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
        # if search_type == 0:
        #     query_image, detected = object_detection(query_image=query_image)
        result = predict(query_image, request_num, search_type, detected)

        app_nums = []
        for info in result:
            # info[1] format: 4020020037823.jpg
            app_num = parse_application_number(info[1])
            app_nums.append(app_num)

        # encoding request image to base64
        raw_image = Image.open(request.FILES['file']).convert('RGB')
        query_image_base64 = base64_encoder(raw_image)

        # response object
        res = {
            "request_num": request_num,
            "request_image": query_image_base64,
            "result_app_numbers": app_nums
        }

        return JsonResponse(data=json.dumps(res), status=200, safe=False)





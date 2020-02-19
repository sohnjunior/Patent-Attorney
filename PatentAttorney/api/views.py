from django.views.generic import View
from django.http import JsonResponse

from .ai.utils import predict

import base64
from io import BytesIO
from PIL import Image
import json
import os


STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')


# -- 등록된 특허 정보 반환
class ApiPatentList(View):
    pass


# -- 특허 이미지 유사도 분석 결과 반환
class ApiPatentPredict(View):

    def post(self, request, *args, **kwargs):
        request_num = int(request.POST['selected'])  # 사용자가 요청한 유사 이미지 개수
        result = predict(request.FILES['file'], request_num)

        # static folder 에 이미지 데이터 구성해놓고 결과 이미지 로드해서 반환해주기
        img_binary = []
        for info in result:
            img_path = os.path.join(STATIC_PATH, info[1])
            raw_image = Image.open(img_path).convert('RGB')  # gray scale 로 읽히는 이미지들이 있어서 RGB로 바꿔줌

            # convert PIL image to base64 string
            buffer = BytesIO()
            raw_image.save(buffer, format='JPEG')
            img_str = base64.b64encode(buffer.getvalue()).decode('ascii')
            img_binary.append(img_str)

        # response object
        res = {"request_num": request_num,
               "images": img_binary}

        return JsonResponse(data=json.dumps(res), status=200, safe=False)





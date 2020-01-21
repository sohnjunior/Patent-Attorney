from django.views.generic import View
from django.http import JsonResponse

from .ai.utils import predict


# -- 등록된 특허 정보 반환
class ApiPatentList(View):
    pass


# -- 특허 이미지 유사도 분석 결과 반환
class ApiPatentPredict(View):

    def post(self, request, *args, **kwargs):
        result = predict(request.FILES['file'], 5)
        print(result)

        # static folder 에 이미지 데이터 구성해놓고 결과 이미지 로드해서 반환해주기

        return JsonResponse(data={"hello": "world"}, status=200)





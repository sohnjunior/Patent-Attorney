import json
import urllib.request
import xml.etree.ElementTree as elemTree

import os
import django
import datetime


# Python 이 실행될 때 DJANGO_SETTINGS_MODULE 라는 환경 변수에 현재 프로젝트의 settings.py 파일 경로를 등록
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# 이제 장고를 가져와 장고 프로젝트를 사용할 수 있도록 환경을 만듬
django.setup()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(BASE_DIR, 'pa-server/config/secrets.json')) as f:
    secrets = json.load(f)


def get_secret(setting, secrets=secrets):
    """ OPEN API 키 추출 """
    try:
        return secrets[setting]
    except KeyError:
        error_msg = f'Set the {setting} env variable.'
        raise ImproperlyConfigured(error_msg)


def parse_xml(xml_string_data, category):
    """ xml 데이터를 파싱해서 필요한 데이터만 추출 """
    root = elemTree.fromstring(xml_string_data)

    # parsing result dictionary
    keys = set(category)
    parsed = dict.fromkeys(keys, 'empty')

    try:
        body = root.find('body')
        items = body.find('items')
        item = items.find('item')

        # iterate all tags
        for child in item:
            if child.tag in category:
                if child.text:
                    parsed[child.tag] = child.text

    except Exception as e:
        header = root.find('header')
        result_code = header.find('resultCode').text
        error_msg = header.find('resultMsg').text
        print(f'특허청 호출 에러 코드[{result_code}] : {error_msg}')

    return parsed


def make_query_string(application_number, mode):
    """ query string 생성 """
    service_key = get_secret("OPENAPI_KEY")
    necessary = '?serviceKey=' + service_key + '&applicationNumber=' + application_number

    if mode == 0:
        option = '&application=true&registration=true&refused=true' \
             '&expiration=true&refused=true&expiration=true&withdrawal=true' \
             '&publication=true&cancel=true&abandonment=true&trademark=true' \
             '&serviceMark=true&trademarkServiceMark=true&businessEmblem=true' \
             '&collectiveMark=true&internationalMark=true&character=true&figure=true' \
             '&compositionCharacter=true&figureComposition=true'
    else:
        option = '&open=true&rejection=true&destroy=true' \
             '&cancle=true&notice=true&registration=true&invalid=true' \
             '&abandonment=true&simi=true&part=true&etc=true' \
             '&destroy=true'

    query_string = necessary + option
    return query_string


def request_open_api(application_number, mode):
    """ 특허청 open api 호출 함수 """
    # request url
    if mode == 0:
        url = 'http://kipo-api.kipi.or.kr/openapi/service/trademarkInfoSearchService/getAdvancedSearch'
        queryParams = make_query_string(application_number=application_number, mode=mode)
        category = ['title', 'bigDrawing']
    else:
        url = 'http://kipo-api.kipi.or.kr/openapi/service/designInfoSearchService/getAdvancedSearch'
        queryParams = make_query_string(application_number=application_number, mode=mode)
        category = ['articleName', 'imagePathLarge']

    # request and get response
    req = urllib.request.Request(url + queryParams)
    response = urllib.request.urlopen(req)
    response_body = response.read()

    # parse xml data
    # 상표명 혹은 물품 명칭, 이미지 url, 출원인이름, 대리인이름, 출원상태, 공고일자, 공고번호
    category += ['applicantName', 'agentName', 'applicationStatus', 'publicationDate', 'publicationNumber']
    return parse_xml(xml_string_data=response_body.decode('utf-8'), category=category)


# TODO 닭과 의자 특허 정보 db에 저장
from api.models import MarkPatentInfo, DesignPatentInfo

if __name__ == '__main__':
    mode = 0
    app_num = str(4020020037823)
    data = request_open_api(str(4020020037823), mode)
    print(data)

    # convert to YYYY-MM-DD format
    pub_date = datetime.datetime.strptime(data['publicationDate'], "%Y%m%d").date()

    if mode == 0:
        MarkPatentInfo.objects.create(title=data['title'], app_num=app_num, app_name=data['applicantName'],
                                      app_status=data['applicationStatus'], pub_date=pub_date,
                                      pub_num=data['publicationNumber'], image_path=data['bigDrawing'])
    else:
        DesignPatentInfo.objects.create(article_name=data['title'], app_num=app_num, app_name=data['applicantName'],
                                        app_status=data['applicationStatus'], pub_date=pub_date,
                                        pub_num=data['publicationNumber'], image_path=data['imagePathLarge'])

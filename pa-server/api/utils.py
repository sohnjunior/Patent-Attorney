import base64
from io import BytesIO
from PIL import Image

import os
import json
import platform
import urllib.request
import xml.etree.ElementTree as elemTree


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(BASE_DIR, 'config/secrets.json')) as f:
    secrets = json.load(f)


def get_secret(setting, secrets=secrets):
    """ OPEN API 키 추출 """
    try:
        return secrets[setting]
    except KeyError:
        error_msg = f'Set the {setting} env variable.'
        raise ImproperlyConfigured(error_msg)


def base64_encoder(image):
    """ PIL image to base64 data """
    buffer = BytesIO()
    image.save(buffer, format='JPEG')
    img_str = base64.b64encode(buffer.getvalue()).decode('ascii')
    return img_str


def parse_application_number(path):
    """ parse the application number """
    if platform.system() == 'Windows':
        parsed = path.split('\\')[3].split('.')[0]
    else:
        parsed = path.split('/')[3].split('.')[0]
    # if it contains 'M' in application number, remove after M
    if parsed.find('M') != -1:
        parsed = parsed.split('M')[0]
    return parsed


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
        print('parsing xml error : ', e)

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
        category = ['title']
    else:
        url = 'http://kipo-api.kipi.or.kr/openapi/service/designInfoSearchService/getAdvancedSearch'
        queryParams = make_query_string(application_number=application_number, mode=mode)
        category = ['articleName']

    # request and get response
    req = urllib.request.Request(url + queryParams)
    response = urllib.request.urlopen(req)
    response_body = response.read()
    print(response_body)
    # parse xml data
    # 상표명 혹은 물품 명칭, 출원인이름, 대리인이름, 출원상태, 공고일자, 공고번호
    category += ['applicantName', 'agentName', 'applicationStatus', 'publicationDate', 'publicationNumber']
    return parse_xml(xml_string_data=response_body.decode('utf-8'), category=category)


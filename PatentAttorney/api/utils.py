import base64
from io import BytesIO
from PIL import Image

import urllib.request
import xml.etree.ElementTree as elemTree


def base64_encoder(image):
    """ PIL image to base64 data """
    buffer = BytesIO()
    image.save(buffer, format='JPEG')
    img_str = base64.b64encode(buffer.getvalue()).decode('ascii')
    return img_str


def parse_application_number(path):
    """ parse the application number """
    parsed = path.split('/')[3].split('.')[0]
    # if it contains 'M' in application number, remove after M
    if parsed.find('M') != -1:
        parsed = parsed.split('M')[0]
    return parsed


def parse_xml(xml_string_data, category):
    """ xml 데이터를 파싱해서 필요한 데이터만 추출 """
    root = elemTree.fromstring(xml_string_data)

    body = root.find('body')
    item = body.find('items').find('item')

    # parsing result dictionary
    keys = set(category)
    parsed = dict.fromkeys(keys, '')

    # iterate all tags
    for child in item:
        if child.tag in category:
            if child.text:
                parsed[child.tag] = child.text
            else:
                parsed[child.tag] = 'empty'

    return parsed


def make_query_string(application_number):
    """ query string 생성 """
    service_key = 'HC1X0Rp%2BrQOhhGVukHovgYtK178YRaCF%2BvCen1bu6SGsWFsIJavPYw78HC4ht69KeedxeIDCnLiKvzUuOIT5LA%3D%3D'
    necessary = '?serviceKey=' + service_key + '&applicationNumber=' + application_number
    option = '&application=true&registration=true&refused=true' \
             '&expiration=true&refused=true&expiration=true&withdrawal=true' \
             '&publication=true&cancel=true&abandonment=true&trademark=true' \
             '&serviceMark=true&trademarkServiceMark=true&businessEmblem=true' \
             '&collectiveMark=true&internationalMark=true&character=true&figure=true' \
             '&compositionCharacter=true&figureComposition=true'

    query_string = necessary + option
    return query_string


def request_open_api(application_number):
    """ 특허청 open api 호출 함수 """
    # request url
    url = 'http://kipo-api.kipi.or.kr/openapi/service/trademarkInfoSearchService/getAdvancedSearch'
    queryParams = make_query_string(application_number=application_number)

    # request and get response
    req = urllib.request.Request(url + queryParams)
    response = urllib.request.urlopen(req)
    response_body = response.read()

    # parse xml data
    # 상표명, 출원인이름, 대리인이름, 출원상태, 공고일자, 공고번호
    category = ['title', 'applicantName', 'agentName', 'applicationStatus', 'publicationDate', 'publicationNumber']
    return parse_xml(xml_string_data=response_body.decode('utf-8'), category=category)

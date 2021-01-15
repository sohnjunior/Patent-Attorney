import base64
from io import BytesIO


def base64_encoder(image):
    """ PIL image to base64 data """
    buffer = BytesIO()
    image.save(buffer, format='JPEG')
    img_str = base64.b64encode(buffer.getvalue()).decode('ascii')
    return img_str


def parse_application_number(path):
    """ parse the application number """
    parsed = path.split('.')[0]
    # if it contains 'M' in application number, remove after M
    if parsed.find('M') != -1:
        parsed = parsed.split('M')[0]
    return parsed

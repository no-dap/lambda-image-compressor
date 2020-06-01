import json
import os
from io import BytesIO

import boto3
from PIL import Image

MAX_SIZE = (1080, 810)
BUCKET_NAME = os.getenv("BUCKET_NAME", "TODO")
AWS_REGION = os.getenv("AWS_REGION", "ap-northeast-2")
s3_client = boto3.client('s3', region_name=AWS_REGION)


def _post_to_s3(byte_string, size, path, name, extension):
    img = Image.open(BytesIO(byte_string))

    if img.mode != 'RGB':
        img = img.convert('RGB')

    img.thumbnail(size, Image.ANTIALIAS)
    output = BytesIO()
    img.save(output, format=extension, quality=100)
    output.seek(0)

    key = f'{path}/{name}.{extension}'
    s3_client.put_object(Bucket=BUCKET_NAME, Key=key, Body=output)


def lambda_handler(payloads, context):
    """
    Create compressed image from origin && save to S3
    :param payloads: dict
    {
        "image": utf-8 encoded byte string,
        "path": string, path of target image,
        "name": string, name of image
    }
    :return: void
    """
    _image = bytes(payloads.get('image'), encoding='utf8')
    _path = payloads.get('path')
    _name = payloads.get('name')
    _origin_img_name, _extension = _name.rsplit('.', 1)
    _post_to_s3(_image, MAX_SIZE, _path, _name, _extension)

    for prefix, size in ('xs', (100, 100)), ('sm', (200, 200)), ('md', (400, 400)), ('lg', (800, 800)):
        _name = f'{prefix}_{_origin_img_name}'
        _post_to_s3(_image, size, _path, _name, _extension)

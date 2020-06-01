import os
from io import BytesIO

from libs import boto3
from libs.PIL import Image

MAX_SIZE = (1080, 810)
BUCKET_NAME = os.getenv("BUCKET_NAME", "TODO")
AWS_REGION = os.getenv("AWS_REGION", "ap-northeast-2")
s3_client = boto3.client('s3', region_name=AWS_REGION)


def lambda_handler(payloads, context):
    """
    Create compressed image from origin && save to S3
    :param payloads: dict
    {
        "image": byte string,
        "path": string, path of target image
    }
    :return: void
    """
    image = payloads.get('image')
    path = payloads.get('path')
    origin_img_name, extension = image.name.rsplit('.', 1)
    img = Image.open(image)

    if img.mode != 'RGB':
        img = img.convert('RGB')

    img.thumbnail(MAX_SIZE, Image.ANTIALIAS)
    output = BytesIO()
    img.save(output, format=extension, quality=100)
    s3_client.put_object(Bucket=BUCKET_NAME, Key=f'{path}/{origin_img_name}.{extension}', Body=output)

    for prefix, size in ('xs', (100, 100)), ('sm', (200, 200)), ('md', (400, 400)), ('lg', (800, 800)):
        img = Image.open(image)

        if img.mode != 'RGB':
            img = img.convert('RGB')

        img.thumbnail(size, Image.ANTIALIAS)
        output = BytesIO()
        img.save(output, format=extension, quality=100)

        img_name = f'{prefix}_{origin_img_name}.{extension}'
        s3_client.put_object(Bucket=BUCKET_NAME, Key=f'{path}/{img_name}', Body=output)

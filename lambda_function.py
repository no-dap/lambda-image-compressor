from io import BytesIO

from libs import boto3
from libs.PIL import Image

MAX_SIZE = (1080, 810)
BUCKET_NAME = 'TODO'
s3_client = boto3.client('s3', region_name='ap-northeast-2')


def compress_image(image, path):
    """
    Create compressed image from origin && save to S3
    :param image: file
    :param path: string, path of target image
    :return: void
    """
    origin_img_name = image.name.rsplit('.', 1)[0]
    img = Image.open(image)

    if img.mode != 'RGB':
        img = img.convert('RGB')

    img.thumbnail(MAX_SIZE, Image.ANTIALIAS)
    output = BytesIO()
    img.save(output, format='JPEG', quality=100)
    s3_client.put_object(Bucket=BUCKET_NAME, Key=f'{path}/{image.name}', Body=output, ContentType='image/jpg')

    for prefix, size in ('xs', (100, 100)), ('sm', (200, 200)), ('md', (400, 400)), ('lg', (800, 800)):
        img = Image.open(image)

        if img.mode != 'RGB':
            img = img.convert('RGB')

        img.thumbnail(size, Image.ANTIALIAS)
        output = BytesIO()
        img.save(output, format='JPEG', quality=100)

        img_name = f'{prefix}_{origin_img_name}.jpg'
        s3_client.put_object(Bucket=BUCKET_NAME, Key=f'{path}/{img_name}', Body=output, ContentType='image/jpg')

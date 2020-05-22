# lambda-image-compressor
Python image compressor using pillow via lambda.

## How to use
1. In project root directory, run script below to install dependency  
```shell script
mkdir libs
pip install --target=./libs -r requirements.txt
```
2. Implement your s3 bucket name inside lambda_function.py.  
in lambda_function.py:  
```python
BUCKET_NAME = 'TODO'
```

3. Create AWS IAM role and grant lambda execute, s3 access privileges.  

## How to run
```python
import boto3


payload = {"TODO": "TODO"}
lambda_client = boto3.client('lambda', aws_access_key_id="TODO", aws_secret_access_key="TODO",
                             region_name='ap-northeast-2')
lambda_client.invoke(FunctionName='image_compressor', Payload=payload, InvocationType='Event')
```
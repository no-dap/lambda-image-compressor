# lambda-image-compressor
Python image compressor using pillow via lambda.

## How to use
1. In project root directory, run script below to install dependency  
```
mkdir libs
pip install --target=./libs -r requirements.txt
```
2. Implement your s3 bucket name inside lambda_function.py.  
in lambda_function.py:  
```
BUCKET_NAME = 'TODO'
```

3. Create AWS IAM role and grant lambda execute, s3 access privileges.  

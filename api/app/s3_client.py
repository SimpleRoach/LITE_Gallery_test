import boto3
from botocore.client import Config

s3 = boto3.client('s3',
                  endpoint_url='https://',
                  aws_access_key_id='0',
                  aws_secret_access_key='0',
                  config=Config(signature_version='s3v4'))

def create_presigned_url(bucket_name, object_name, expiration=3600):
    try:
        response = s3.generate_presigned_url('put_object',
                                             Params={'Bucket': bucket_name,
                                                     'Key': object_name},
                                             ExpiresIn=expiration)
    except Exception as e:
        print(e)
        return None

    return response

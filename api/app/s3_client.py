import aiobotocore
from botocore.client import Config

session = aiobotocore.get_session()

async def create_presigned_url(bucket_name, object_name, expiration=3600):
    async with session.create_client('s3',
                                     endpoint_url='https://s3.storage.selcloud.ru',
                                     aws_access_key_id='9edc6f25afd2420288c148406fceec7e',
                                     aws_secret_access_key='30d28259118b401db0984c1f65c7ef79',
                                     config=Config(signature_version='s3v4')) as s3:
        try:
            response = await s3.generate_presigned_url('put_object',
                                                       Params={'Bucket': bucket_name,
                                                               'Key': object_name},
                                                       ExpiresIn=expiration)
        except Exception as e:
            print(e)
            return None

        return response
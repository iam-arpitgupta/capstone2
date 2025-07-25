"""
shows the connection with the aws account 
"""
import boto3 
import os 

from src.constants import AWS_SECRET_ACCESS_KEY_ENV_KEY, AWS_ACCESS_KEY_ID_ENV_KEY, REGION_NAME

class S3Client:
    s3_client = None
    s3_resource = None

    def __init__(self):
        """
        this class get the aws key from the env variable and create a s3 connectiion with it 
        and rasie exception if the clinet is not set 
        """
        if S3Client.s3_resource == None or S3Client.s3_client == None:
                _access_key_id = os.getenv(AWS_ACCESS_KEY_ID_ENV_KEY)
                _secret_key_id = os.getenv(AWS_SECRET_ACCESS_KEY_ENV_KEY)
                if _access_key_id is None:
                    raise Exception(f"{AWS_ACCESS_KEY_ID_ENV_KEY} is not set")
                if _secret_key_id is None:
                    raise Exception(f"{AWS_SECRET_ACCESS_KEY_ENV_KEY} is not set")
                # will  make a connection with s3 
                S3Client.s3_resource = boto3.resource('s3',
                                            aws_access_key_id=__access_key_id,
                                            aws_secret_access_key=__secret_access_key,
                                            region_name=region_name
                                            )
                S3Client.s3_client = boto3.client('s3',
                                        aws_access_key_id=__access_key_id,
                                        aws_secret_access_key=__secret_access_key,
                                        region_name=region_name
                                        )
        self.s3_resource = S3Client.s3_resource
        self.s3_client = S3Client.s3_client



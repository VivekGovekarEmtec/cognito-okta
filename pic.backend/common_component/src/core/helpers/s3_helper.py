import boto3
from common_component.src.core.utils.Logger import logger

s3_client = boto3.client('s3', region_name='ca-central-1')


def download_file_from_s3(bucket: str, file_key: str, local_file_path: str) -> str:
    try:
        # Download the file
        s3_client.download_file(bucket, file_key, local_file_path)
        logger.info('File downloaded successfully')
        return local_file_path

    except Exception as e:
        logger.info('Exception occurred while downloading template to s3 : ' + str(e))


def upload_file_to_s3(file_path, s3_file_path, bucket_name):
    try:
        s3 = boto3.resource('s3', region_name='ca-central-1')
        s3.Bucket(bucket_name).upload_file(file_path, s3_file_path)

        return s3_file_path
    except Exception as e:
        logger.info('Exception occurred while uploading template to s3 : ' + str(e))

import os
import json
from common_component.src.core.helpers.secrets_manager_helper import get_secret
from common_component.src.core.utils.Logger import logger
from common_component.src.core.helpers.s3_helper import download_file_from_s3

certificate_bucket = os.environ.get('bucket_name')
rds_certificate_file_path = os.environ.get('rds_proxy_ssl_certificate_path')


class Config:
    """ This class is used to configure environment variables"""

    def __init__(self):
        logger.info("Get Credentials from aws secret manager to send ")
        secrets = get_secret()
        # Parse JSON key value pairs.
        secret_cred = json.loads(secrets)
        self.DEBUG: bool = True
        self.APP_HOST: str = secret_cred["rds_proxy_host"]
        self.APP_PORT: int = secret_cred["port"]
        self.WRITER_DB_URL: str = secret_cred["rds_proxy_writer_endpoint"]
        self.READER_DB_URL: str = secret_cred["rds_proxy_reader_endpoint"]
        self.RDS_PROXY_USERNAME: str = secret_cred["username"]
        self.RDS_DATABASE: str = secret_cred["dbClusterIdentifier"]
        self.MEMCACHE_CLUSTER: str = secret_cred["memcache_cluster"]


class CertificateConfig(Config):
    bucket = certificate_bucket
    file_key = rds_certificate_file_path
    local_file_path = file_key.replace("rds_proxy_ssl_certificate/", "/tmp/")
    res = download_file_from_s3(bucket, file_key, local_file_path)
    print(res)
    RDS_PROXY_SSL_CERTIFICATE_NAME = local_file_path


def get_config():
    config_details = CertificateConfig()
    return config_details


config: CertificateConfig = get_config()

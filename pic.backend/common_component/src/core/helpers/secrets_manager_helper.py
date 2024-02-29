import base64
import json
import boto3
from common_component.src.core.helpers.ssm_helper import get_ssm_parameter
from common_component.src.core.utils.Logger import logger


def get_secret():
    secrets_parameter = get_ssm_parameter('/pic/secret_manager_details')
    secrets_parameter_json = json.loads(secrets_parameter)
    secret_name = secrets_parameter_json["secret_name"]
    region_name = secrets_parameter_json["region"]
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except Exception as e:
        logger.error('Exception occurred while getting secrets : ', str(e))
        raise e

    else:
        # Decrypts secret using the associated KMS key.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            return secret
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            return decoded_binary_secret

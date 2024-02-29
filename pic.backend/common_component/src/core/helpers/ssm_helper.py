import boto3
from common_component.src.core.utils.Logger import logger


def get_ssm_parameter(parameter_name, decrypt=True):
    """
    Retrieve a parameter from AWS Systems Manager (SSM) Parameter Store.

    Parameters:
    - parameter_name (str): The name of the parameter to retrieve.
    - decrypt (bool): Whether to decrypt secure string parameters. Default is True.

    Returns:
    - parameter_value (str): The value of the retrieved parameter.
    """
    ssm_client = boto3.client('ssm', region_name='ca-central-1')

    try:
        # Retrieve the parameter value
        response = ssm_client.get_parameter(
            Name=parameter_name,
            WithDecryption=decrypt
        )

        parameter_value = response['Parameter']['Value']

        return parameter_value

    except Exception as e:
        # Handle any exceptions that may occur during parameter retrieval
        logger.error(f"Error retrieving parameter '{parameter_name}': {e}")

        return None


def get_all_parameters_by_path(parameter_paths):
    """
    Retrieve AWS Systems Manager (SSM) parameters based on the provided paths.

    Parameters:
    - parameter_paths (str or list): SSM parameter path(s). Can be a single path as a string or multiple paths as a list.

    Returns:
    - parameters_dictionary (dict): Dictionary containing parameter names and values.
    """
    ssm_client = boto3.client('ssm', region_name='ca-central-1')
    parameters_dictionary = {}

    try:
        if isinstance(parameter_paths, str):
            parameter_paths = [parameter_paths]  # Convert a single path to a list

        for path in parameter_paths:
            # Retrieve parameters recursively for the specified path
            response = ssm_client.get_parameters_by_path(
                Path=path,
                Recursive=True
            )

            # Extract parameters and add them to the dictionary
            parameters = response.get('Parameters', [])
            for param in parameters:
                parameters_dictionary[param["Name"]] = param["Value"]

    except Exception as e:
        # Handle any exceptions that may occur during parameter retrieval
        logger.error(f"Error retrieving parameters: {e}")

    return parameters_dictionary


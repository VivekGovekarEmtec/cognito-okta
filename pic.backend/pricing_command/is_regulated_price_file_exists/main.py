from urllib.parse import unquote
from service import is_regulated_prices_file_exists
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import get_query_param_value, create_response
from common_component.src.core.handlers.exception_handler import sqlalchemy_exception_handler, \
    unhandled_exception_handler, value_exception_handler

log = Log().get_logger_service("Get station information")


@log.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    log.info("Entered into event handler")
    log.set_correlation_id(context.aws_request_id)
    log.append_keys(log_stream=context.log_stream_name)
    log.append_keys(resource_path=event['path'])
    try:
        query_string_params = event["queryStringParameters"]
        base64_data = event["body"]
        file_name: str = get_query_param_value(query_string_params, "file_name", str)

        file_name = unquote(file_name)
        response_data = is_regulated_prices_file_exists(file_name, base64_data)
        log.debug("Received response from is_regulated_prices_file_exists Service")
    except ValueError as ve:
        result = value_exception_handler(ve)
        raise create_response(result)
    except SQLAlchemyError as sae:
        # Catch and handle SQLAlchemy errors
        result = sqlalchemy_exception_handler(sae)
        return create_response(result)
    except Exception as exc:
        # Catch and handle Unhandled errors
        result = unhandled_exception_handler(exc)
        return create_response(result)
    else:
        return create_response(response_data)

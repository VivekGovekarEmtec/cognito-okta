from service import get_price_change_auth_data
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import get_query_param_value, create_response
from common_component.src.core.handlers.exception_handler import sqlalchemy_exception_handler, \
    unhandled_exception_handler

log = Log().get_logger_service("Get price change auth data")


@log.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    log.info("Entered into event handler")
    log.set_correlation_id(context.aws_request_id)
    log.append_keys(log_stream=context.log_stream_name)
    log.append_keys(resource_path=event['path'])
    try:
        query_string_params = event["queryStringParameters"]
        lang = get_query_param_value(query_string_params, "lang", str)
        user_id = get_query_param_value(query_string_params, "user_id", str)
        response_data = get_price_change_auth_data(lang, user_id)
        log.debug("Received response from get_price_change_auth_data Service")
        if not response_data['data']['price_change_auth_data']:
            response_data["status_code"] = 204
            response_data["data"] = []
            return create_response(response_data)
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

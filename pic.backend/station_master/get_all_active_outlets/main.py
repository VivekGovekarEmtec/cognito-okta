from sqlalchemy.exc import SQLAlchemyError
from service import get_all_active_outlet
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import get_query_param_value
from common_component.src.core.helpers.helper import create_response
from common_component.src.core.handlers.exception_handler import sqlalchemy_exception_handler, unhandled_exception_handler
log = Log().get_logger_service("station master getallActiveOutlets")


@log.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    log.debug("Entered into get__active_outlet Router")
    log.set_correlation_id(context.aws_request_id)
    log.append_keys(log_stream=context.log_stream_name)
    log.append_keys(resource_path=event['path'])
    try:
        query_string_params = event["queryStringParameters"]
        language = get_query_param_value(query_string_params, "language", str)
        result = get_all_active_outlet(language)
        log.debug("Received response from getallActiveOutlets Service")

    except SQLAlchemyError as sae:
        # Catch and handle SQLAlchemy errors
        result = sqlalchemy_exception_handler(sae)
        return create_response(result)
    except Exception as exc:
        # Catch and handle Unhandled errors
        result = unhandled_exception_handler(exc)
        return create_response(result)
    else:
        return create_response(result)

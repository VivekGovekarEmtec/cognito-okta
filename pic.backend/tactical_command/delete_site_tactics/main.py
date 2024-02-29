from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import create_response, get_query_param_value
from common_component.src.core.handlers.exception_handler import sqlalchemy_exception_handler, unhandled_exception_handler
from service import delete_site_tactics

log = Log().get_logger_service("Delete site tactics")


@log.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    log.info("Entered into delete_site_tactics event handler")
    log.set_correlation_id(context.aws_request_id)
    log.append_keys(log_stream=context.log_stream_name)
    log.append_keys(resource_path=event['path'])
    try:
        query_string_params = event["queryStringParameters"]
        id = get_query_param_value(query_string_params, "id", int)
        delete_site_tactics_response = delete_site_tactics(id)
        log.debug("Received response from delete site tactics Service")

    except SQLAlchemyError as sae:
        # Catch and handle SQLAlchemy errors
        result = sqlalchemy_exception_handler(sae)
        return create_response(result)
    except Exception as exc:
        # Catch and handle Unhandled errors
        result = unhandled_exception_handler(exc)
        return create_response(result)
    else:
        return create_response(delete_site_tactics_response)

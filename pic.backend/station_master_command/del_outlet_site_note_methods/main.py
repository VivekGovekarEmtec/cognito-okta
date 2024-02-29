from sqlalchemy.exc import SQLAlchemyError
from aws_lambda_powertools.utilities.typing import LambdaContext
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import get_query_param_value, create_response
from common_component.src.core.handlers.exception_handler import sqlalchemy_exception_handler, unhandled_exception_handler
from service import delete_notification


log = Log().get_logger_service("Get all unreviewed survey")


@log.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    log.info("Entered into event handler")
    log.set_correlation_id(context.aws_request_id)
    log.append_keys(log_stream=context.log_stream_name)
    log.append_keys(resource_path=event['path'])
    try:
            query_string_params = event["queryStringParameters"]
            id = get_query_param_value(query_string_params, "id",int)
            user_id = get_query_param_value(query_string_params, "user_id",str)
            response_data = delete_notification(id,user_id)
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


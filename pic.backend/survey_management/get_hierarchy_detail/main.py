from service import get_hierarchy_detail
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import get_query_param_value, create_response
from common_component.src.core.handlers.exception_handler import sqlalchemy_exception_handler, unhandled_exception_handler

log = Log().get_logger_service("Get Hierarchy Detail")


@log.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    log.info("Entered into event handler")
    log.set_correlation_id(context.aws_request_id)
    log.append_keys(log_stream=context.log_stream_name)
    try:
        query_string_params = event["queryStringParameters"]
        hierarchy_id = get_query_param_value(query_string_params, "hierarchy_id", int)
        product_id = get_query_param_value(query_string_params, "product_id", str)
        response_data = get_hierarchy_detail(hierarchy_id, product_id)    
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
 
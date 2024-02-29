from service import delete_outlet_product_configuration
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import get_query_param_value, create_response
from common_component.src.core.handlers.exception_handler import sqlalchemy_exception_handler, unhandled_exception_handler

log = Log().get_logger_service("Delete Outlet Product Configuration")

@log.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    log.info("Entered into event handler")
    log.set_correlation_id(context.aws_request_id)
    log.append_keys(log_stream=context.log_stream_name)
    try:
        log.append_keys(resource_path="/master/product/deleteOutletProductConfiguration")
        log.debug("Entered into delete_outlet_product_configuration Router")
        query_string_params = event["queryStringParameters"]
        id = get_query_param_value(query_string_params, "id", int)
        user_id = get_query_param_value(query_string_params, "user_id", str)
        delete_product = delete_outlet_product_configuration(id, user_id)
        log.debug("Received response from delete_outlet_product_configuration Service") 
    except SQLAlchemyError as sae:
            # Catch and handle SQLAlchemy errors
        result = sqlalchemy_exception_handler(sae)
        return create_response(result)
    except Exception as exc:
            # Catch and handle Unhandled errors
        result = unhandled_exception_handler(exc)
        return create_response(result)
    else:
        return create_response(delete_product)

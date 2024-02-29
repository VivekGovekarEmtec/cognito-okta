from service import valid_price_change
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import get_query_param_value, create_response
from common_component.src.core.handlers.exception_handler import sqlalchemy_exception_handler, \
    unhandled_exception_handler

log = Log().get_logger_service("Get Price Change Validation")


@log.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    log.info("Entered into event handler")
    log.set_correlation_id(context.aws_request_id)
    log.append_keys(log_stream=context.log_stream_name)
    log.append_keys(resource_path=event['path'])
    try:
        query_string_params = event["queryStringParameters"]
        site_id = get_query_param_value(query_string_params, "site_id", int)
        product_id = get_query_param_value(query_string_params, "product_id", int)
        price = get_query_param_value(query_string_params, "price", float)
        site_list = get_query_param_value(query_string_params, "site_list", str)
        is_request_now = get_query_param_value(query_string_params, "is_request_now", bool)
        request_date = get_query_param_value(query_string_params, "request_date", str)

        response_data = valid_price_change(site_id, product_id, price, site_list, is_request_now, request_date)
        log.debug("Received response from valid_price_change Service")
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

from datetime import datetime
from service import site_price_on_hold_by_site_id_delete
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import get_query_param_value, create_response
from common_component.src.core.handlers.exception_handler import sqlalchemy_exception_handler, \
    unhandled_exception_handler

log = Log().get_logger_service("Delete price on hold")


@log.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    log.info("Entered into event handler")
    log.set_correlation_id(context.aws_request_id)
    log.append_keys(log_stream=context.log_stream_name)
    log.append_keys(resource_path=event['path'])
    try:
        query_string_params = event["queryStringParameters"]
        site_no: int = get_query_param_value(query_string_params, "site_no", int)
        product_id: int = get_query_param_value(query_string_params, "product_id", int)
        user_current_date: datetime = get_query_param_value(query_string_params, "user_current_date", str)
        user_id: str = get_query_param_value(query_string_params, "user_id", str)
        response_data = site_price_on_hold_by_site_id_delete(site_no, product_id, user_current_date, user_id)
        log.debug("Received response from site_price_on_hold_by_site_id_delete Service")

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

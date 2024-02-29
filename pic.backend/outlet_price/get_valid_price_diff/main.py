from decimal import Decimal
from service import get_valid_price_diff
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import get_query_param_value, create_response
from common_component.src.core.handlers.exception_handler import (sqlalchemy_exception_handler,
                                                                  unhandled_exception_handler)

log = Log().get_logger_service("get valid price diff")


@log.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    log.info("Entered into event handler")
    log.set_correlation_id(context.aws_request_id)
    log.append_keys(log_stream=context.log_stream_name)
    log.append_keys(resource_path=event['path'])
    try:
        query_string_params = event["queryStringParameters"]
        site_id = get_query_param_value(query_string_params, "site_id", int)
        requested_price = get_query_param_value(query_string_params, "requested_price", Decimal)
        product_id = get_query_param_value(query_string_params, "product_id", int)
        language = get_query_param_value(query_string_params, "language", str)

        valid_diff = get_valid_price_diff(
            site_id=site_id, requested_price=requested_price, product_id=product_id, lang=language)
        log.debug("Received response from get_valid_price_diff Service")
        if valid_diff['data']['is_diff_greater_than_max'] is not False and valid_diff['data']['is_diff_greater_than_max'] is not True:
            response = {
                "status_code": 204,
                "message": "Data not found in the database",
                "data": None
            }
            return response
        if not valid_diff['data']['max_diff_value']:
            response = {
                "status_code": 204,
                "message": "Data not found in the database",
                "data": None
            }
            return response
    except SQLAlchemyError as sae:
        # Catch and handle SQLAlchemy errors
        result = sqlalchemy_exception_handler(sae)
        return create_response(result)
    except Exception as exc:
        # Catch and handle Unhandled errors
        result = unhandled_exception_handler(exc)
        return create_response(result)
    else:
        return create_response(valid_diff)

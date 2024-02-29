from service import site_price_on_hold_json_insert
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import create_response
from common_component.src.core.handlers.exception_handler import sqlalchemy_exception_handler, \
    unhandled_exception_handler
from schema import PriceOnHoldInsertList
from aws_lambda_powertools.utilities.parser import parse

log = Log().get_logger_service("Insert price on hold")


@log.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    log.info("Entered into event handler")
    log.set_correlation_id(context.aws_request_id)
    log.append_keys(log_stream=context.log_stream_name)
    log.append_keys(resource_path=event['path'])
    try:
        request = event["body"]
        parsed_payload: PriceOnHoldInsertList = parse(event=request, model=PriceOnHoldInsertList)
        response_data = site_price_on_hold_json_insert(parsed_payload)
        log.debug("Received response from site_price_on_hold_json_insert Service")

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

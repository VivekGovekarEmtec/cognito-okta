import os
from service import validation, save_price_change
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import create_response
from common_component.src.core.handlers.exception_handler import sqlalchemy_exception_handler, \
    unhandled_exception_handler
from schema import SiteProductPriceChange
from aws_lambda_powertools.utilities.parser import parse

log = Log().get_logger_service("Reset price change")


@log.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    log.info("Entered into event handler")
    log.set_correlation_id(context.aws_request_id)
    log.append_keys(log_stream=context.log_stream_name)
    log.append_keys(resource_path=event['path'])
    try:
        request = event["body"]
        parsed_payload: SiteProductPriceChange = parse(event=request, model=SiteProductPriceChange)
        validation_path = os.environ.get('VALIDATION_ROUTE')
        save_reset_price_path = os.environ.get('SAVE_RESET_PRIZE_ROUTE')
        if event['path'] == validation_path:
            response_data = validation(parsed_payload)
        elif event['path'] == save_reset_price_path:
            response_data = save_price_change(parsed_payload)
        else:
            response_data = {
                "status_code": 404,
                "message": "Invalid api",
                "data": {}
            }
        log.debug("Received response from validation Service")

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

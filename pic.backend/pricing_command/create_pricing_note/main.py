from service import save_note
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import create_response
from common_component.src.core.handlers.exception_handler import sqlalchemy_exception_handler, \
    unhandled_exception_handler
from schema import CreatePricingNote
from aws_lambda_powertools.utilities.parser import parse

log = Log().get_logger_service("Create price on hold")


@log.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    log.info("Entered into event handler")
    log.set_correlation_id(context.aws_request_id)
    log.append_keys(log_stream=context.log_stream_name)
    log.append_keys(resource_path=event['path'])
    try:
        request = event["body"]
        parsed_payload: CreatePricingNote = parse(event=request, model=CreatePricingNote)
        response_data = save_note(parsed_payload)
        log.debug("Received response from save_note Service")

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

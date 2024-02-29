from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import create_response
from common_component.src.core.handlers.exception_handler import sqlalchemy_exception_handler, \
    unhandled_exception_handler
from aws_lambda_powertools.utilities.parser import parse
from service import update_site_tactics
from schema import SiteTacticUpdate

log = Log().get_logger_service("Update Site Tactics")


@log.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    log.info("Entered into event handler")
    log.set_correlation_id(context.aws_request_id)
    log.append_keys(log_stream=context.log_stream_name)
    log.append_keys(resource_path=event['path'])
    try:
        """
        This is a router function used to save regulated price
        """
        log.append_keys(resource_path="/master/regulatedPrice/saveRegulatedPrice")
        log.debug("Entered into save_regulated_prices Router")
        request = event['body']

        parsed_payload: SiteTacticUpdate = parse(event=request, model=SiteTacticUpdate)
        update_site_tactics_response = update_site_tactics(parsed_payload)
        log.debug("Received response from update_site_tactics Service")
    except SQLAlchemyError as sae:
        # Catch and handle SQLAlchemy errors
        result = sqlalchemy_exception_handler(sae)
        return create_response(result)
    except Exception as exc:
        # Catch and handle Unhandled errors
        result = unhandled_exception_handler(exc)
        return create_response(result)
    else:
        return create_response(update_site_tactics_response)


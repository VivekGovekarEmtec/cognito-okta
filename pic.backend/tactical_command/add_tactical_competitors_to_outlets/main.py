from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import create_response, get_query_param_value
from common_component.src.core.handlers.exception_handler import sqlalchemy_exception_handler, unhandled_exception_handler
from service import add_tactic_competitors_for_outlets
from schema import AddTacticCompetitorsForOutlets
from aws_lambda_powertools.utilities.parser import parse

log = Log().get_logger_service("Add tactic competitors to outlet")


@log.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    log.info("Entered into event handler")
    log.set_correlation_id(context.aws_request_id)
    log.append_keys(log_stream=context.log_stream_name)
    log.append_keys(resource_path=event['path'])
    try:
        request = event['body']
        parsed_payload: AddTacticCompetitorsForOutlets = parse(event=request, model=AddTacticCompetitorsForOutlets)
        new_competitors_added_to_outlets = add_tactic_competitors_for_outlets(parsed_payload)
        log.debug("Received response from add_tactic_competitors_for_outlets Service")

    except SQLAlchemyError as sae:
        # Catch and handle SQLAlchemy errors
        result = sqlalchemy_exception_handler(sae)
        return create_response(result)
    except Exception as exc:
        # Catch and handle Unhandled errors
        result = unhandled_exception_handler(exc)
        return create_response(result)
    else:
        return create_response(new_competitors_added_to_outlets)

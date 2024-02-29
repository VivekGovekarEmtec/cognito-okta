from service import is_site_tactic_time_overlap
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import get_query_param_value, create_response
from common_component.src.core.handlers.exception_handler import (sqlalchemy_exception_handler,
                                                                  unhandled_exception_handler)

log = Log().get_logger_service("is Site Tactic Time Overlap")


@log.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    log.info("Entered into event handler")
    log.set_correlation_id(context.aws_request_id)
    log.append_keys(log_stream=context.log_stream_name)
    log.append_keys(resource_path=event['path'])
    try:
        query_string_params = event["queryStringParameters"]
        site_id = get_query_param_value(query_string_params, "site_id", int)
        follow_action_id = get_query_param_value(query_string_params, "follow_action_id", int)
        id = get_query_param_value(query_string_params, "id", int)
        start_time = get_query_param_value(query_string_params, "start_time", str)
        end_time = get_query_param_value(query_string_params, "end_time", str)

        response_data = is_site_tactic_time_overlap(site_id, follow_action_id, id, start_time, end_time)

        log.debug("Received response from is_site_tactic_time_overlap Service")
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

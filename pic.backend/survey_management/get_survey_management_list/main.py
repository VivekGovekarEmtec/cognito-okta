from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import get_query_param_value, create_response
from common_component.src.core.handlers.exception_handler import sqlalchemy_exception_handler, unhandled_exception_handler
from service import get_frequency_grid
log = Log().get_logger_service("Get Survey Management List")


@log.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    log.info("Entered into event handler")
    log.set_correlation_id(context.aws_request_id)
    log.append_keys(log_stream=context.log_stream_name)
    try:
        query_string_params = event["queryStringParameters"]
        site_id = get_query_param_value(query_string_params, "site_id", str)
        language = get_query_param_value(query_string_params, "language",str)
        active_inactive_code = get_query_param_value(query_string_params, "active_inactive_code", str)
        search_term = get_query_param_value(query_string_params, "search_term", str)
        sort_name = get_query_param_value(query_string_params, "sort_name", str)
        sort_direction = get_query_param_value(query_string_params, "sort_direction", str)
        page_number = get_query_param_value(query_string_params, "page_number", int)
        records = get_query_param_value(query_string_params, "records", int)

        log.debug("Entered into get_survey_management_list Router")
        get_survey_manage_list = get_frequency_grid(site_id, language, active_inactive_code,
                                                                              search_term, sort_name, sort_direction,
                                                                              page_number, records)
        log.debug("Received response from get_frequency_grid Service")
        response_data = (get_survey_manage_list)
            
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
        

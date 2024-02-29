import service
from enum import Enum

from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import get_query_param_value, create_response
from common_component.src.core.handlers.exception_handler import sqlalchemy_exception_handler, unhandled_exception_handler
from common_component.src.core.helpers.helper import  SortDirections


log = Log().get_logger_service("Get Associated Competitors")
@log.inject_lambda_context(log_event=True)

def lambda_handler(event, context):

    """
    This api is used to get all competitors
    """
    try:
        log.debug("Entered into get associated competitors Router")
        query_string_params = event["queryStringParameters"] 
        search_term: str = get_query_param_value(query_string_params, "search_term", str)
        outlet_id: int = get_query_param_value(query_string_params, "outlet_id", int) 
        language: str = get_query_param_value(query_string_params, "language", str)
        response_data  = service.get_associated_competitors(search_term=search_term,
                                                                                             outlet_id=outlet_id,
                                                                                             language=language)
        log.debug("Received response from get_associated_competitors Service")

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

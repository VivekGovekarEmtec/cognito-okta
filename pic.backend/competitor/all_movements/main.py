import service
import traceback
from enum import Enum

from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import get_query_param_value, create_response
from common_component.src.core.handlers.exception_handler import sqlalchemy_exception_handler, unhandled_exception_handler
from common_component.src.core.helpers.helper import  SortDirections


log = Log().get_logger_service("All Movements")
@log.inject_lambda_context(log_event=True)

def lambda_handler(event, context):

    """
    This api is to get site All Movements
    """
    try:

        log.debug("Entered All Movements")
        query_string_params = event["queryStringParameters"] 
        

        site_id: int = get_query_param_value(query_string_params, "site_id", int)
        is_editable: bool = get_query_param_value(query_string_params, "is_editable" , bool)
        language: str = get_query_param_value(query_string_params, "language", str)

        response_data = service.get_site_tactical_movements(site_id, language, is_editable)
        log.debug("Received response from all movements Service")

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
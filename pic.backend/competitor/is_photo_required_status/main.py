import service
import traceback
from enum import Enum

from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import get_query_param_value, create_response
from common_component.src.core.handlers.exception_handler import sqlalchemy_exception_handler, unhandled_exception_handler
from common_component.src.core.helpers.helper import  SortDirections


log = Log().get_logger_service("Is Photo Required Status")
@log.inject_lambda_context(log_event=True)

def lambda_handler(event, context):

    """
    This api returns photo required status
    """
    try:
        log.debug("Entered into is_photo_required_status Router")
        query_string_params = event["queryStringParameters"] 
        site_id: int = get_query_param_value(query_string_params, "site_id", int)

        response_data = service.is_photo_required_status(site_id)
        log.debug("Received response from is_photo_required_status Service")

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
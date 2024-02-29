import service
import traceback
from enum import Enum

from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import get_query_param_value, create_response
from common_component.src.core.handlers.exception_handler import sqlalchemy_exception_handler, unhandled_exception_handler
from common_component.src.core.helpers.helper import  SortDirections


class SortName(str, Enum):
    stationNumber = "stationNumber"
    brandName = "brandName"
    address = "address"
    municipalityName = "municipalityName"
    siteRating = "siteRating"
    km = "km"
    stationnumber = ""

log = Log().get_logger_service("Search Competitors")
@log.inject_lambda_context(log_event=True)

def lambda_handler(event, context):
    """
    This api is used to search competitors by outlet id
    """

    try:
        query_string_params = event["queryStringParameters"] 
        
        search_term: str = get_query_param_value(query_string_params, "search_term", str),
        sort_name: SortName = get_query_param_value(query_string_params, "sort_name", str),

        sort_direction: SortDirections = get_query_param_value(query_string_params, "sort_direction", str),
        outlet_id: int = get_query_param_value(query_string_params, "outlet_id", int),
        language: str = get_query_param_value(query_string_params, "language", str),
        page_number: int = get_query_param_value(query_string_params, "page_number", int),
        records: int = get_query_param_value(query_string_params, "records", int)
        log.debug("Entered into search Competitors Router")

        response_data = service.find_competitors(search_term, sort_name, sort_direction,
                                                                       language, page_number, records, outlet_id)
        log.debug("Received response from find_competitors Service")

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

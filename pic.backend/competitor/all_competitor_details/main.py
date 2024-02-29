import service
from enum import Enum
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import get_query_param_value, create_response
from common_component.src.core.handlers.exception_handler import sqlalchemy_exception_handler, unhandled_exception_handler
from common_component.src.core.helpers.helper import  SortDirections

log = Log().get_logger_service("Get Associated Competitors")
@log.inject_lambda_context(log_event=True)

class SortName(str, Enum):
    kentId = "kentId"
    gasBuddy = "gasBuddy"
    brand = "brand"
    address = "address"
    marketer = "marketer"
    muniName = "muniName"
    province = "province"
    latitude = "latitude"
    longitude = "longitude"
    isResDiesel = "isResDiesel"
    lsdSign = "lsdSign"
    siteRating = "siteRating"
    ml = "ml"
    statusDesc = "statusDesc"
    wdHours = "wdHours"
    kentid = ""

def lambda_handler(event, context):
    """
    This api will return all competitor details
    """

    query_string_params = event["queryStringParameters"] 

    try:
        search_term: str = get_query_param_value(query_string_params, "search_term", str)
        sort_name: SortName = get_query_param_value(query_string_params, "sort_name", str)
        sort_direction: SortDirections = get_query_param_value(query_string_params, "sort_direction", str)
        language: str = get_query_param_value(query_string_params, "language", str)
        page_number: int = get_query_param_value(query_string_params, "page_number", int)
        records: int = get_query_param_value(query_string_params, "records", int)
        log.debug("Entered into competitors_details")
        response_data = service.get_all_competitors_details(search_term, sort_name, sort_direction,
                                                                          language, page_number, records)
        log.debug("Received response from get_all_competitors_details Service")

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
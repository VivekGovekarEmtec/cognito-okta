from sqlalchemy import text
import json
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import remove_keys
from common_component.src.core.helpers.encoder import jsonable_encoder

db_instance = CreateDBConnection()
log = Log().get_logger_service()

def get_frequency_grid(site_id: str, language: str, active_inactive_code: str, search_term: str | None, sort_name: str,
                       sort_direction: str, page_number: int, records: int):
    """
    This function is used to get the list of survey management frequencies based on site id.
    """
    try:
        log.append_keys(service_function="get_frequency_grid")
        log.debug("Entered into get_frequency_grid service")
        with db_instance.create_writer_connection() as db:
            get_frequency_grid_function_name = "dbo.fn_survey_management_grouped"
            param_dict = {
                "site_id": site_id,
                "language": language,
                "status": active_inactive_code,
                "search_term": search_term,
                "sort_name": sort_name,
                "sort_direction": sort_direction,
                "page_number": page_number,
                "records": records
            }
            query = text(
                'SELECT * FROM '
                + get_frequency_grid_function_name +
                '(:site_id,'
                ':language,'
                ':search_term,'
                ':sort_name,'
                ':sort_direction,'
                ':page_number,'
                ':records,'
                ':status)')
            output = call_postgres_function(query=query, db=db, parameters=param_dict)
        
        response_data = jsonable_encoder(output)
        # Get the counts in local variables
        total_search_count = response_data[0]["total_search_count"]
        total_count = response_data[0]["total_count"]
        # Remove total fields from response data
        updated_resp = remove_keys(response_data, "total_search_count")
        response_data = remove_keys(updated_resp, "total_count")
        check_none = all(x is None for data in response_data for x in data.values())
        if total_count is None or total_count == 0:
            response = {
            "status_code":204,
            "message": "Total count is 0",
            "data": None
        }
        if check_none is True:
            response_data = []
        else :
         response = {
            "status_code":200,
            "message": "Received frequency data from database successfully",
            "data": {"total_search_count": total_search_count, "total_count": total_count,
                     "survey_management_list": response_data}
        }   
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        return response

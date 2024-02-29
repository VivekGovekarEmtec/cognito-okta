import json
from sqlalchemy import text
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.encoder import jsonable_encoder
from common_component.src.core.helpers.helper import remove_keys

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service()

def get_all_competitors_details(search_term: str, sort_name: str, sort_direction: str, language: str, page_number: int, records: int):
    """
    This api is used to get all competitors
    """
    try:
        log.append_keys(service_function="get_all_competitors_details")
        log.debug("Entered into get_all_competitors_details service")
        with db_instance.create_writer_connection() as db:
            get_competitors_function_name = 'dbo.fn_competitor_detail_list'
            query = text(
                "SELECT * from " + get_competitors_function_name + "(cast(:language AS character varying),:search_term,cast(:sort_name AS character varying),cast(:sort_direction AS character varying),:page_number,:records)")
            parameters = {"search_term": search_term, "sort_name": sort_name, "sort_direction": sort_direction, "language": language, "page_number": page_number, "records": records}
            output = call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        response_data = jsonable_encoder(output)

        # Get the counts in local variables
        total_search_count = response_data[0]["total_search_count"]
        total_count = response_data[0]["total_count"]
        # Remove total fields from response data
        updated_resp = remove_keys(response_data, "total_search_count")
        response_data = remove_keys(updated_resp, "total_count")
        check_none = all(x is None for data in response_data for x in data.values())
        if check_none is True:
            response_data = []

        if len(response_data) == 0:
            response = {
            "status_code": 204,
            "message": "Data not found in the database",
            "data": None
        }
        else:
            response = {
            "status_code": 200,
            "message": "Received all competitors data from Database successfully",
            "data": {"total_search_count": total_search_count, "total_count": total_count, "competitor_detail_list": response_data}
        }
    except Exception as exc:
        raise exc
    else:
        log.debug("get_all_competitors_details service executed successfully")
        return response
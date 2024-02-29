import json
from sqlalchemy import text
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.encoder import jsonable_encoder
from common_component.src.core.helpers.helper import remove_keys

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service()

def get_associated_competitors(search_term: str, language: str, outlet_id: int):
    """
    This function will search for competitors
    """
    try:
        log.append_keys(service_function="get_associated_competitors")
        log.debug("Entered into get_associated_competitors service")
        with db_instance.create_writer_connection() as db:
            associated_competitors_function_name = 'dbo.fn_competitor_association'
            query = text(
                "select * from " + associated_competitors_function_name + "(:outlet_id,cast(:language AS character varying),cast(:search_term AS character varying))")
            parameters = {"outlet_id": outlet_id, "search_term": search_term,
                          "language": language}
            output = call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")

        # Get the counts in local variables
        response_data = jsonable_encoder(output)
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
            "message": "Received search associated competitor data from Database successfully",
            "data": {"total_search_count": total_search_count, "total_count": total_count,
                     "associated_competitors_list": response_data}
        }
    except Exception as exc:
        raise exc
    else:
        log.debug("get_associated_competitors service executed successfully")
        return response
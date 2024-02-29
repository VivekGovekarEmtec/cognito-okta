from sqlalchemy import text
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
import json
from common_component.src.core.helpers.encoder import jsonable_encoder

db_instance = CreateDBConnection()
log = Log().get_logger_service("Survey schedule")

def get_hierarchy_by_site_id(site_id: int, language: str):
    """
        This function is used to get hierarchy based on given site id
    """
    try:
        with db_instance.create_writer_connection() as db:
            get_hierarchy_by_site_id_function_name = "dbo.fn_hierarchy_by_site_id"
            param_dict = {"site_id": site_id, "lang": language}
            query = text(
                'SELECT * FROM '
                + get_hierarchy_by_site_id_function_name + '(:site_id, :lang)')
            output = call_postgres_function(query=query, db=db, parameters=param_dict)

        log.debug("Received response from database")
        hierarchy_by_site_id =output[0]['hierarchy_type_id']
        response_data = jsonable_encoder(output)

        if not hierarchy_by_site_id:
            response = {
            "status_code": 204,
            "message": "Data not found in the database",
            "data": None
        }
        else:
            response = {
                "status_code": 200,
                "message": "Received marketers data from Database successfully",
                "data": {"hierarchy_by_site_id": response_data}
            }
    except Exception as exc:
        raise exc
    else:
        log.debug("get_hierarchy_by_site_id service executed successfully")
        return response

import json
from sqlalchemy import text

from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.encoder import jsonable_encoder

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service()

def is_photo_required_status(site_no: int):
    """
    This function will return photo required status
    """
    try:
        log.debug("Entered into is_photo_required_status service")
        with db_instance.create_writer_connection() as db:
            is_photo_required_status_function_name = 'dbo.fn_site_photo_required_select_by_site_no'
            query = text("select * from " + is_photo_required_status_function_name + "(:site_no)")
            parameters = {"site_no": site_no}
            output = call_postgres_function(query=query, parameters=parameters, db=db)
        response_data = jsonable_encoder(output)
        log.debug("Received response from database")
        if len(response_data) == 0:
            response = {
            "status_code": 204,
            "message": "Data not found in the database",
            "data": None
        }
        else:
            response = {
            "status_code": 200,
            "message": "Received is photo required data from Database successfully",
            "data": {"is_photo_required_status": response_data[0]}
        }
    except Exception as exc:
        raise exc
    else:
        log.debug("is_photo_required_status service executed successfully")
        return response

def auto_clear_site_status(site_id: int):
    """
    This api get auto clear site status data from database
    """
    try:
        log.append_keys(service_function="auto_clear_site_status")
        log.debug("Entered into auto_clear_site_status service")
        with db_instance.create_writer_connection() as db:
            auto_clear_site_status_function_name = 'dbo.fn_site_configuration_auto_clear_select_by_site_no'
            query = text("select * from " + auto_clear_site_status_function_name + "(:site_id)")
            parameters = {"site_id": site_id}
            output = call_postgres_function(query=query, parameters=parameters, db=db)
        response_data = jsonable_encoder(output)
        log.debug("Received response from database")
        response_data = jsonable_encoder(output)
        if len(response_data) == 0:
            response = {
            "status_code": 204,
            "message": "Data not found in the database",
            "data": None
        }
        else:
            response = {
            "status_code": 200,
            "message": "Received auto clear site status data from Database successfully",
            "data": {"auto_clear_site_status": response_data[0]}
        }

    except Exception as exc:
        raise exc
    else:
        log.debug("auto_clear_site_status service executed successfully")
        return response
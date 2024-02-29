from sqlalchemy import text
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.encoder import jsonable_encoder

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service("Station master GetOutletDetailsByOutletNo")


def get_notification_types(language: str):
    """
    This function will return notification types
    """
    try:
        log.append_keys(service_function="get_notification_types")
        log.debug("Entered into get_notification_types service")
        with db_instance.create_writer_connection() as db:
            get_outlet_function_name = 'dbo.fn_site_notification_types'
            query = text("SELECT * from " + get_outlet_function_name + "(:_lang)")
            parameters = {"_lang": language}
            response_data = call_postgres_function(query=query, db=db, parameters=parameters)
        if len(response_data) == 0:
            log.debug("No data found in database")

            response = {
                "status_code": 204,
                "message": "No data found in database",
                "data": {}
            }
        else:
            log.debug("Received response from database")
            response = {
                "status_code": 200,
                "message": "Received notification types from Database successfully",
                "data": {"notification_types_list": jsonable_encoder(response_data)}
            }
    except Exception as e:
        raise e
    else:
        log.debug("get_notification_types service executed successfully")
        return response
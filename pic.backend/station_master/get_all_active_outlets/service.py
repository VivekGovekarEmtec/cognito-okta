from sqlalchemy import text
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.encoder import jsonable_encoder
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service("station master getallActiveOutlets")


def get_all_active_outlet(language: str):
    """
    This function is used to return all outlets
    """
    try:
        log.append_keys(service_function="get_all_active_outlet")
        log.debug("Entered into get_all_active_outlet service")
        with db_instance.create_writer_connection() as db:
            get_all_outlet_function_name = 'dbo.fn_all_active_outlets'
            query = text("SELECT * from " + get_all_outlet_function_name + "(:_lang)")

            parameters = {"_lang": language}
            output = call_postgres_function(query, parameters, db)
        log.debug("Received response from database")
        response_data = jsonable_encoder(output)
        response = {
            "status_code": 200,
            "message": "Received all active outlet from database successfully",
            "data": {"all_active_outlet": eval(response_data[0]['site_no'])}
        }
    except Exception as exc:
        raise exc
    else:
        log.debug("get_all_active_outlet service executed successfully")
        return response
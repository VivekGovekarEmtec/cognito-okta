from sqlalchemy import text
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.encoder import jsonable_encoder
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service("outlet price get_is_daily_reset_applicable")


def get_is_daily_reset_applicable(site_id: int):
    try:
        log.append_keys(service_function="get_is_daily_reset_applicable")
        log.debug("Entered into get_is_daily_reset_applicable service")
        with db_instance.create_writer_connection() as db:
            warning_function_name = "dbo.fn_is_daily_reset_applicable"
            param_dict = {
                "site_id": site_id
            }
            query = text(
                'SELECT * FROM ' + warning_function_name + '(:site_id)'
            )
            output = call_postgres_function(query=query, parameters=param_dict, db=db)
        log.debug("Received response from database")
        response_data = jsonable_encoder(output)
        if len(response_data) != 0:
            response = {
                "status_code": 200,
                "message": "Received is daily reset applicable data from database successfully",
                "data": response_data[0]
                }   
        else:
            response = {
                "status_code": 204,
                "message": "No data found in database",
                "data": {}
            }
    except Exception as exc:
        raise exc
    else:
        log.debug("get_is_daily_reset_applicable service executed successfully")
        return response
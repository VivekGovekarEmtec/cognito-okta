from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.helpers.encoder import jsonable_encoder
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service("get site warning")


def get_price_hold_warning(site_id: int, timezone_code: str):
    try:
        log.append_keys(service_function="get_price_hold_warning")
        log.debug("Entered into get_price_hold_warning service")
        with db_instance.create_reader_connection() as db:
            warning_function_name = "dbo.fn_site_warning"
            param_dict = {
                "site_id": site_id,
                "timezone_code": timezone_code
            }
            query = text(
                'SELECT * FROM ' + warning_function_name + '(:site_id,:timezone_code)'
            )
            output = call_postgres_function(query=query, parameters=param_dict, db=db)
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
                "message": "Received price hold warning data from database successfully",
                "data": response_data
            }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        log.debug("get_price_hold_warning service executed successfully")
        return response

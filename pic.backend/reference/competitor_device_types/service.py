from sqlalchemy import text
import json
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.encoder import jsonable_encoder

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service()


def get_competitor_device_types(language: str):
    """
    This function is used to return all competitor device types data
    """
    try:
        log.append_keys(service_function="get_competitor_device_types")
        log.debug("Entered into get_competitor_device_types service")
        with db_instance.create_reader_connection() as db:
            get_competitor_device_types_function_name = 'dbo.fn_competitor_device_types'
            query = text("SELECT * FROM " + get_competitor_device_types_function_name + "(:language)")
            param_dict = {"language": language}
            output = call_postgres_function(query=query, db=db, parameters=param_dict)
        log.debug("Received response from database")
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
                "message": "Received competitor device types data from Database successfully",
                "data": {"competitor_device_types_list": response_data}
            }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        return response



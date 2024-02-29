from sqlalchemy import text
import json
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.encoder import jsonable_encoder

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service()


def get_site_rating():
    """
    This function is used to return all site ratings data
    """
    try:
        log.append_keys(service_function="get_site_rating")
        log.debug("Entered into get_site_rating service")
        with db_instance.create_reader_connection() as db:
            function_name = 'dbo.fn_site_ratings'
            query = text("SELECT * FROM " + function_name + "()")
            output = call_postgres_function(query=query, db=db)
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
                "message": "Received Site Rating data from Database successfully",
                "data": {"site_rating_list": response_data}
            }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        return response



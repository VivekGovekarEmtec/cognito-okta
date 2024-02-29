from sqlalchemy import text
import json
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.encoder import jsonable_encoder

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service()


def get_diesel_restriction(kent_id_list: str):
    """
    This function is used to check whether diesel is restricted for given list of kent_id's
    """
    try:
        log.append_keys(service_function="get_diesel_restriction")
        log.debug("Entered into get_diesel_restriction service")
        with db_instance.create_writer_connection() as db:
            get_diesel_restriction_function_name = "dbo.fn_competitor_diesel_restriction"
            param_dict = {"kent_id_list": kent_id_list}
            query = text(
                'SELECT * FROM '
                + get_diesel_restriction_function_name + '(:kent_id_list)')
            output = call_postgres_function(query=query, db=db, parameters=param_dict)
        response_data = jsonable_encoder(output)
        response = {
            "status_code": 200,
            "message": "Received diesel restriction data from database successfully",
            "data": {"diesel_restriction_list": response_data}
        }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        return response

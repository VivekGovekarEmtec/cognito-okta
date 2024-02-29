from sqlalchemy import text
import json
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.encoder import jsonable_encoder

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service()


def is_available_kent_id(kent_id: int):
    """
    This returns true if kent id is available and 0 if kent id is not available
    """
    try:
        log.append_keys(service_function="is_available_kent_id")
        log.debug("Entered into is_available_kent_id service")
        with db_instance.create_reader_connection() as db:
            get_outlet_function_name = 'dbo.fn_is_available_kent_id'
            query = text("select * from " + get_outlet_function_name + "(:kent_id)")
            parameters = {"kent_id": kent_id}
            output = call_postgres_function(query=query, parameters=parameters, db=db)
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
                "message": "Received kent id data from Database successfully",
                "data": {"is_available_kent_id": response_data[0]}
            }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        return response



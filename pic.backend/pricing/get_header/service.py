from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.encoder import jsonable_encoder

log = Log().get_logger_service("Get Header")
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()


def get_regulated_prices_headers(authorization_number):
    """
    This API is used to get regulated price headers
    """
    try:
        log.append_keys(service_function="get_regulated_prices_headers")
        log.debug("Entered into get_regulated_prices_headers service")
        with db_instance.create_writer_connection() as db:
            parameters = {"authorization_number": authorization_number}
            get_regulated_prices_headers_function_name = 'dbo.fn_regulated_prices_header_select'
            query = text("select * from " + get_regulated_prices_headers_function_name + '(:authorization_number)')
            output = call_postgres_function(
                query=query, parameters=parameters, db=db)
        response_data = jsonable_encoder(output)
        log.debug("Received response from database")
        response = {
            "status_code": 200,
            "message": "Received regulated price headers data from Database successfully",
            "data": {
                "regulated_prices_headers_list": response_data
            }
        }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        log.debug("get_regulated_prices_headers service executed successfully")
        return response

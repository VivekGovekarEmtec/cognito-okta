from sqlalchemy import text
from common_component.src.core.helpers.encoder import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log

db_instance = CreateDBConnection()
log = Log().get_logger_service()


def get_all_regulated_reference_values():
    """
    This function is used to get regulated reference values for nova scotia
    """
    try:
        log.append_keys(service_function="get_all_regulated_reference_values")
        log.debug("Entered into get_all_regulated_reference_values service")
        with db_instance.create_writer_connection() as db:
            regulated_reference_function_name = 'dbo.fn_regulated_prices_reference_values'
            query = text(
                'SELECT * FROM ' + regulated_reference_function_name +
                '()')
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
                "message": "Received regulated reference values from database successfully",
                "data": {"regulated_reference_values": response_data}
            }

    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception

    except Exception as exc:
        raise exc
    else:
        log.debug("get_all_regulated_reference_values service executed successfully")
        return response

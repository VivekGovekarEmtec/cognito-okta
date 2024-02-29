from sqlalchemy import text
import json
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.encoder import jsonable_encoder

log = Log().get_logger_service("Get regulated prize details service")
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()


# reset price change
def get_regulated_prices_details(authorization_number, lang):
    """
    This API is used to get regulated pricing details
    """
    try:
        log.append_keys(service_function="get_regulated_prices_details")
        log.debug("Entered into get_regulated_prices_details service")
        with db_instance.create_writer_connection() as db:

            # Get data for margins
            parameters = {"authorization_number": authorization_number, "lang": lang}
            get_regulated_prices_details_function_name = 'dbo.fn_regulated_prices_details_select'
            query = text(
                "select * from " + get_regulated_prices_details_function_name + '(:authorization_number,cast(:lang AS '
                                                                                'character varying))')
            output = call_postgres_function(
                query=query, parameters=parameters, db=db)

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
                "message": "Received regulated price details from Database successfully",
                "data": {
                    "regulated_prices_details_list": response_data
                }
            }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        log.debug("get_regulated_prices_details service executed successfully")
        return response

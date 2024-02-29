from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.helpers.encoder import jsonable_encoder
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log


log = Log().get_logger_service("price_on_hold_validation")
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()


def price_on_hold_validation(site_id: int, product_id: int):
    """
    This function is used to check for give site_id price is on hold or not
    """
    try:
        log.append_keys(service_function="price_on_hold_validation")
        log.debug("Entered into price_on_hold_validation service")
        with db_instance.create_reader_connection() as db:
            price_hold_function_name = 'dbo.fn_is_price_on_hold'
            parameters = {
                "site_id": site_id,
                "product_id": product_id,
            }
            query = text(
                'SELECT * FROM ' + price_hold_function_name +
                '(:site_id,:product_id)'
            )
            output = call_postgres_function(query=query, parameters=parameters, db=db)
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
                "message": "Received price on hold validation from Database successfully",
                "data": {"competitors": response_data}
            }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        return response



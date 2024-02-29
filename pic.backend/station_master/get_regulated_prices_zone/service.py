from sqlalchemy import text
from common_component.src.core.helpers.encoder import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log

db_instance = CreateDBConnection()
log = Log().get_logger_service()


def get_regulated_price_zone(language: str):
    """
    This function is used to return all regulated price zones
    """
    try:
        log.append_keys(service_function="get_regulated_price_zone")
        log.debug("Entered into get_regulated_price_zone service")
        with db_instance.create_writer_connection() as db:
            get_regulated_price_zone_function_name = 'dbo.fn_regulated_prices_zones'
            query = text("SELECT * from " + get_regulated_price_zone_function_name + "(:language)")

            parameters = {"language": language}
            output = call_postgres_function(query, parameters, db)
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
                "message": "Received regulated price zone from Database successfully",
                "data": {"regulated_price_zone": response_data}
            }
    except SQLAlchemyError as sql_alchemy_exception:
        raise sql_alchemy_exception

    except Exception as exc:
        raise exc

    else:
        log.debug("get_regulated_price_zone service executed successfully")
        return response

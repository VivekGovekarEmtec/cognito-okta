from sqlalchemy import text
import json
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.encoder import jsonable_encoder

log = Log().get_logger_service("Get station info for reset price")
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()


# reset price change
def get_station_info(outlet_ids: str, lang: str):
    """
    This API is used to get station information
    """
    try:
        log.append_keys(service_function="get_station_info")
        log.debug("Entered into get_station_info service")
        with db_instance.create_reader_connection() as db:
            get_function_name = 'dbo.fn_get_stations_current_price'

            query = text(
                "SELECT * from " + get_function_name + "(CAST(:outlet_ids AS character varying), CAST(:lang AS character varying))")
            parameters = {"outlet_ids": outlet_ids, 'lang': lang}

            output = call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        response_data = jsonable_encoder(output)

        response = {
            "status_code": 200,
            "message": "get the price information successfully",
            "data": {"reset_price_list": response_data}
        }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        log.debug("get_station_info service executed successfully")
        return response

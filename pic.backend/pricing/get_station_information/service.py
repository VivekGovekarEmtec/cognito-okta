import json
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.encoder import jsonable_encoder

log = Log().get_logger_service("Get station information")
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()


# price change auth
def get_station_information(outlet_ids: str, product_id: int, current_date: datetime, lang: str):
    """
    This API is used to get station information
    """
    try:
        log.append_keys(service_function="get_station_information")
        log.debug("Entered into get_station_information service")
        with db_instance.create_writer_connection() as db:
            get_function_name = 'dbo.fn_get_stations_price_on_hold_select'
            query = text(
                "SELECT * from " + get_function_name + "(CAST(:outlet_ids AS character varying), :product_id, CAST(:current_date AS timestamp without time zone), CAST(:lang AS character varying))")
            parameters = {"outlet_ids": outlet_ids, 'product_id': product_id, 'current_date': current_date,
                          'lang': lang}
            output = call_postgres_function(query=query, parameters=parameters, db=db)

        log.debug("Received response from database")

        # Load JSON directly
        response_data = jsonable_encoder(output)

        # Check for None values in loaded JSON data
        check_none = all(
            value is json.loads('null') for value in dict(zip(iter(response_data), iter(response_data))).values())
        if check_none:
            response_data = []

        response = {
            "status_code": 200,
            "message": "get the station information successfully",
            "data": {"station_information_data": response_data}
        }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        log.debug("get_station_information service executed successfully")
        return response

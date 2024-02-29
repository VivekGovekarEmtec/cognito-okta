from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.encoder import jsonable_encoder

log = Log().get_logger_service("Get regulated prize details service")
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()


# reset price change
def get_outlet_price_bulloch(site_id, lang):
    """
    This API is used to get bulloch prices
    """
    try:
        log.append_keys(service_function="get_outlet_price_bulloch")
        log.debug("Entered into get_outlet_price_bulloch service")
        with db_instance.create_writer_connection() as db:
            # Get data for margins
            parameters = {"site_id": site_id, "lang": lang}
            get_bulloch_price_function_name = 'dbo.fn_bulloch_product_price_change'
            query = text("select * from " + get_bulloch_price_function_name + '(:site_id,cast(:lang AS '
                                                                              'character varying))')
            output = call_postgres_function(
                query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        response_data = jsonable_encoder(output)
        if len(response_data) == 0:
            response = {
                "status_code": 204,
                "message": "Data not found in the database",
                "data": None
            }
        else:
            if isinstance(response_data, list) and len(response_data) == 1:
                response_data = response_data[0]
            response = {
                "status_code": 200,
                "message": "Received bulloch price data from Database successfully",
                "data": {
                    "bulloch": jsonable_encoder(response_data)
                }
            }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        log.info("get_outlet_price_bulloch service executed successfully")
        return response

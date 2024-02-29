from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.encoder import jsonable_encoder

log = Log().get_logger_service("Get regulated prize details service")
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()


# reset price change
def get_scheduled_price_changes(site_id, lang):
    """
        This API is used to get scheduled prices
        """
    try:
        log.append_keys(service_function="get_scheduled_price_changes")
        log.debug("Entered into get_scheduled_price_changes service")
        with db_instance.create_writer_connection() as db:

            # Get data for margins
            parameters = {"site_id": site_id, "lang": lang}
            get_scheduled_price_changes_function_name = 'dbo.fn_site_product_price_changes'
            query = text("select * from " + get_scheduled_price_changes_function_name + '(:site_id,cast(:lang AS '
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
            response = {
                "status_code": 200,
                "message": "Received scheduled price data from Database successfully",
                "data": {
                    "scheduled_price": jsonable_encoder(response_data)
                }
            }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        log.info("get_scheduled_price_changes service executed successfully")
        return response

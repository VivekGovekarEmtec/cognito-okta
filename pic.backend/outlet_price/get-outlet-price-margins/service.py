from sqlalchemy import text
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.encoder import jsonable_encoder
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service("outlet price get_outlet_price_margins")


def get_outlet_price_margins(site_id, lang):
    """
    This API is used to get outlet price margins
    """
    try:
        log.append_keys(service_function="get_outlet_price_margins")
        log.debug("Entered into get_outlet_price_margins service")
        with db_instance.create_writer_connection() as db:

            parameters = {"site_id": site_id, "lang": lang}
            get_site_price_changes_margins_function_name = 'dbo.fn_site_product_price_changes_margins'
            query = text("select * from " + get_site_price_changes_margins_function_name + '(:site_id,cast(:lang AS '
                                                                                           'character varying))')
            output = call_postgres_function(
                query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        margin_response_data = jsonable_encoder(output)
        if isinstance(margin_response_data, list) and len(margin_response_data) != 0:
            response = {
                "status_code": 200,
                "message": "Received margin price data from Database successfully",
                "data": {
                    "margins": margin_response_data
                }
            }   
        else:
            response = {
                "status_code": 204,
                "message": "No data found in database",
                "data": {}
            }
    except Exception as exc:
        raise exc
    else:
        log.debug("get_outlet_price_margins service executed successfully")
        return response
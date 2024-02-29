from sqlalchemy import text
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.encoder import jsonable_encoder
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service("outlet price getOutletCompetitorPrice")


def get_outlet_competitor_price(site_id, lang):
    """
    This API is used to get pricing notes
    """
    try:
        log.append_keys(service_function="get_outlet_competitor_price")
        log.debug("Entered into get_outlet_competitor_price service")
        with db_instance.create_writer_connection() as db:

            # Get data for margins
            parameters = {"site_id": site_id, "lang": lang}
            get_competitor_price_function_name = 'dbo.fn_screen_competitor_price_survey_select'
            query = text("select * from " + get_competitor_price_function_name + '(:site_id,cast(:lang AS '
                                                                                 'character varying))')
            output = call_postgres_function(
                query=query, parameters=parameters, db=db)
        log.debug("Received response from database")

        response_data = jsonable_encoder(output)
        if isinstance(response_data, list) and len(response_data) != 0:
            response = {
                "status_code": 200,
                "message": "Received competitor price data from Database successfully",
                "data": {
                    "competitors_survey_price_list": response_data
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
        log.debug("get_outlet_competitor_price service executed successfully")
        return response
from sqlalchemy import text
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.encoder import jsonable_encoder

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service("Get outlet detail by outlet id")


def get_outlet_detail_by_site_id(site_id: int, language: str, user_id: str):
    """
    This function is used to return all outlets
    """
    try:
        log.append_keys(service_function="get_outlet_detail_by_site_id")
        log.debug("Entered into get_outlet_detail_by_site_id service")

        with db_instance.create_writer_connection() as db:
            get_outlet_by_site_no_function_name = 'dbo.fn_site_detail_by_site_no'
            query = text("SELECT * from " + get_outlet_by_site_no_function_name + "(:site_id, :language, :user_id)")

            parameters = {"site_id": site_id, "language": language, "user_id": user_id}
            output = call_postgres_function(query, parameters, db)
        log.debug(f"Received response from database{output}")
        response_data = jsonable_encoder(output[0])
    except Exception as exc:
        raise exc
    else:
        log.debug("get_outlet_detail_by_site_id service executed successfully")
        return response_data


def get_outlet_price(site_id, lang):
    """
    This API is used to get outlet prices
    """
    try:
        log.append_keys(service_function="get_outlet_price")
        log.debug("Entered into get_outlet_price service")
        with db_instance.create_writer_connection() as db:

            # Get data for margins
            parameters = {"site_id": site_id, "lang": lang}
            get_price_function_name = 'dbo.fn_screen_site_product_price_changes_price'
            query = text("select * from " + get_price_function_name + '(:site_id,cast(:lang AS '
                                                                      'character varying))')
            output = call_postgres_function(
                query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        response_data = jsonable_encoder(output)
        if isinstance(response_data, list) and len(response_data) == 1:
            response_data = response_data[0]
        response = {"price": jsonable_encoder(response_data)}
    except Exception as exc:
        raise exc
    else:
        log.debug("get_outlet_price service executed successfully")
        return response


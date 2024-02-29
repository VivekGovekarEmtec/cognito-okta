from sqlalchemy import text
import json
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.component.services.cache_service import cache_manage_service
from common_component.src.core.helpers.encoder import jsonable_encoder

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service()


def get_tactic_pricing_zone(product_id: int, language: str):
    """
    This function is used to return all tactic pricing zone data
    """
    try:
        log.append_keys(service_function="get_tactic_pricing_zone")
        log.debug("Entered into get_tactic_pricing_zone service")
        # Check if the object is already present in DB. Using None string to check the default value.
        key = "tactic_pricing_zone_list" + '_' + language.lower()
        response = cache_manage_service.get_cached_data(key, "None")
        resp = response['data'][key]
        if resp == "None":
            with db_instance.create_reader_connection() as db:
                function_name = 'dbo.fn_tactic_pricing_zone'
                query = text("SELECT * FROM " + function_name + "(:product_id, :language)")
                param_dict = {"product_id": product_id, "language": language}
                output = call_postgres_function(query=query, db=db, parameters=param_dict)
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
                    "message": "Received tactic pricing zone data from database successfully",
                    "data": {"tactic_pricing_zone_list": response_data}
                }
        else:
            log.info("Received response from memcached")
            response = {
                "status_code": 200,
                "message": "Received tactic price data from memcached successfully",
                "data": {"tactic_pricing_zone_list": resp}
            }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        return response



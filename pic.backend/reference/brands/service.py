from sqlalchemy import text
import json
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import title_case
from common_component.src.component.services.cache_service import cache_manage_service
from common_component.src.core.helpers.encoder import jsonable_encoder

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service()


def get_brands(language: str):
    """
    This function is used to return brands
    """
    try:
        log.append_keys(service_function="get_brands")
        log.debug("Entered into get_brands service")
        # Check if the object is already present in DB. Using None string to check the default value.
        key = "brands_list" + '_' + language.lower()
        response = cache_manage_service.get_cached_data(key, "None")
        resp = response['data'][key]
        if resp == "None":
            with db_instance.create_reader_connection() as db:
                get_brands_function_name = 'dbo.fn_brands'
                query = text("SELECT * from " + get_brands_function_name + "(:language)")
                parameters = {"language": language}
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
                for brands in response_data:
                    brands['brand_name'] = title_case(brands['brand_name'])
                response = {
                    "status_code": 200,
                    "message": "Received brands data from database successfully",
                    "data": {"brands_list": response_data}
                }
        else:
            log.info("Received response from memcached")
            response = {
                "status_code": 200,
                "message": "Received brands data from memcached successfully",
                "data": {"brands_list": resp}
            }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        return response



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


def get_province(language: str, country_code='CA'):
    """
    This function is used to return province
    """
    try:
        log.append_keys(service_function="get_province")
        log.debug("Entered into get_province service")
        # Check if the object is already present in DB. Using None string to check the default value.
        key = "province_list" + '_' + language.lower()
        response = cache_manage_service.get_cached_data(key, "None")
        resp = response['data'][key]
        if resp == "None":
            with db_instance.create_reader_connection() as db:
                get_province_function_name = 'dbo.fn_provinces'
                query = text("SELECT * from " + get_province_function_name + "(:language)")
                parameters = {"language": language}
                output = call_postgres_function(query=query, parameters=parameters, db=db)
                output_list = jsonable_encoder(output)
                filtered_list = list(filter(lambda i: i["country_code"] == country_code, output_list))
            log.debug("Received response from database")
            if len(filtered_list) == 0:
                response = {
                    "status_code": 204,
                    "message": "Data not found in the database",
                    "data": None
                }
            else:
                response = {
                    "status_code": 200,
                    "message": "Received province data from database successfully",
                    "data": {"province_list": filtered_list}
                }
        else:
            log.info("Received response from memcached")
            response = {
                "status_code": 200,
                "message": "Received province data from memcached successfully",
                "data": {"province_list": resp}
            }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        return response



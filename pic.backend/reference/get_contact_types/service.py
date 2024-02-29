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


def get_contact_types(language: str):
    """
    This function will get contact types from database
    """
    try:
        log.append_keys(service_function="get_contact_types")
        log.debug("Entered into get_contact_types service")
        # Check if the object is already present in DB. Using None string to check the default value.
        key = "contact_types_list" + '_' + language.lower()
        response = cache_manage_service.get_cached_data(key, "None")
        resp = response['data'][key]
        if resp == "None":
            with db_instance.create_reader_connection() as db:
                get_contact_types_function_name = 'dbo.fn_contact_types'
                query = text("SELECT * from " + get_contact_types_function_name + "(:_lang)")
                parameters = {"_lang": language}
                output = call_postgres_function(query=query, db=db, parameters=parameters)
            response_data = jsonable_encoder(output)
            log.debug("Received response from database")
            if len(response_data) == 0:
                response = {
                    "status_code": 204,
                    "message": "Data not found in the database",
                    "data": None
                }
            else:
                response = {
                    "status_code": 200,
                    "message": "Received contacts types from Database successfully",
                    "data": {"contact_types_list": response_data}
                }
        else:
            log.info("Received response from memcached")
            response = {
                "status_code": 200,
                "message": "Received tactic price data from memcached successfully",
                "data": {"contact_types_list": resp}
            }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        return response



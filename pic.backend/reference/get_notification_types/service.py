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


def get_notification_types(language: str):
    """
    This function is used to get the notification types
    """
    try:
        log.append_keys(service_function="get_notification_types")
        log.debug("Entered into get_notification_types service")
        # Check if the object is already present in DB. Using None string to check the default value.
        key = "notification_types" + '_' + language.lower()
        response = cache_manage_service.get_cached_data(key, "None")
        resp = response['data'][key]
        if resp == "None":
            with db_instance.create_reader_connection() as db:
                notification_type_function_name = 'dbo.fn_notification_types'
                parm_dict = {"show_default": None, "language": language}
                query = text(
                    'SELECT * FROM ' + notification_type_function_name +
                    '(CAST(:show_default as smallint),CAST(:language as character varying))')
                output = call_postgres_function(query=query, db=db, parameters=parm_dict)
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
                    "message": "Received notification types from database successfully",
                    "data": {"notification_types": response_data}
                }
        else:
            log.info("Received response from memcached")
            response = {
                "status_code": 200,
                "message": "Received facility types data from memcached successfully",
                "data": {"notification_types": resp}
            }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        return response



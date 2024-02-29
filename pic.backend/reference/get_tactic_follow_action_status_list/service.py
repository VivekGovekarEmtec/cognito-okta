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


def get_tactic_follow_action_status(lang):
    """
        This API is used to get tactic follow action status list
    """
    try:
        log.append_keys(service_function="get_tactic_follow_action_status")
        log.debug("Entered into get_tactic_follow_action_status service")
        # Check if the object is already present in DB. Using None string to check the default value.
        key = "follow_action_status_list" + '_' + lang.lower()
        response = cache_manage_service.get_cached_data(key, "None")
        resp = response['data'][key]
        if resp == "None":
            with db_instance.create_reader_connection() as db:
                # Get data for tactic follow actions status
                parameters = {"lang": lang}
                get_tactic_follow_action_status_function_name = 'dbo.fn_tactic_follow_action_status_list'
                query = text(
                    "select * from " + get_tactic_follow_action_status_function_name + '(cast(:lang AS character varying))')
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
                response = {
                    "status_code": 200,
                    "message": "Received tactic follow action status data from database successfully",
                    "data": {
                        "follow_action_status_list": response_data
                    }
                }
                log.info("Response returned for getTacticFollowActionStatusList API")
        else:
            log.info("Received response from memcached")
            response = {
                "status_code": 200,
                "message": "Received tactic follow action status data from memcached successfully",
                "data": {"follow_action_status_list": resp}
            }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        return response

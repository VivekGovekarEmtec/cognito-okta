from sqlalchemy import text
import json
from common_component.src.core.helpers.encoder import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log

db_instance = CreateDBConnection()
log = Log().get_logger_service()

def is_auto_clear_survey_toggle(site_id: int, user_id: str):
    """
    This api is used for is auto clear survey toggle
    """
    try:
        log.append_keys(service_function="is_auto_clear_survey_toggle")
        log.debug("Entered into is_auto_clear_survey_toggle service")
        with db_instance.create_writer_connection() as db:
            auto_clear_toggle_procedure_name = 'dbo.sp_site_configuration_auto_clear_toggle'
            query = text("call " + auto_clear_toggle_procedure_name + "(:site_id,:user_id)")
            parameters = {"site_id": site_id, "user_id": user_id}
            call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")

        response = {
            "status_code": 200,
            "message": "Is auto clear survey toggle Updated successfully",
            "data": {}
        }
        
    except SQLAlchemyError as sql_alchemy_exception:
        raise sql_alchemy_exception
    
    except Exception as exc:
        raise exc
    else:
        log.debug("is_auto_clear_survey_toggle service executed successfully")
        return jsonable_encoder(response)
from sqlalchemy import text
import json
from common_component.src.core.helpers.encoder import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log

db_instance = CreateDBConnection()
log = Log().get_logger_service()

def is_photo_required_toggle(site_no: int, user_id: str):
    """
    This api is used for is photo required toggle
    """
    try:
        log.append_keys(service_function="is_photo_required_toggle")
        log.debug("Entered into is_photo_required_toggle service")
        with db_instance.create_writer_connection() as db:
            photo_toggle_procedure_name = 'dbo.sp_site_photo_required_toggle'
            query = text("call " + photo_toggle_procedure_name + "(:site_no,:user_id)")
            parameters = {"site_no": site_no, "user_id": user_id}
            call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")

        response = {
            "status_code": 200,
            "message": "Is photo required toggle Updated successfully",
            "data": {}
        }
    except SQLAlchemyError as sql_alchemy_exception:
        raise sql_alchemy_exception
    
    except Exception as exc:
        raise exc
    else:
        log.debug("is_photo_required_toggle service executed successfully")
        return jsonable_encoder(response)
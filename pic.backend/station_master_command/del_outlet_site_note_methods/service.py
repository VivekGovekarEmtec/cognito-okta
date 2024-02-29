from sqlalchemy import text
from schemas.notification_schema import SiteNotification
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
import json
from common_component.src.core.helpers.encoder import jsonable_encoder

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service("Station master command deletenotification")

def delete_notification(id: int, user_id: str):
    """
    This function is used to delete notification
    """
    try:
        log.append_keys(service_function="delete_notification")
        log.debug("Entered into delete_notification service")
        with db_instance.create_writer_connection() as db:
            delete_notification_procedure_name = 'dbo.sp_site_notifications_delete'
            query = text("call " + delete_notification_procedure_name + "(:id,:user_id)")
            parameters = {"id": id, "user_id": user_id}
            call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        response = {
            "status_code": 200,
            "message": "Deleted the site notification successfully",
            "data": {}
        }
    except Exception as e:
        raise e
    else:
        log.debug("delete_notification service executed successfully")
        return jsonable_encoder(response)
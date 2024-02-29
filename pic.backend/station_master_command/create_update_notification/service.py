from sqlalchemy import text
from schemas.notification_schema import SiteNotification
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
import json
from common_component.src.core.helpers.encoder import jsonable_encoder

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service("Station master command create/updatenotification")
def create_site_notification(notification: SiteNotification):
    """
    This function is to create notification
    """
    try:
        log.append_keys(service_function="create_site_notification")
        log.debug("Entered into create_site_notification service")
        with db_instance.create_writer_connection() as db:
            create_site_notification_procedure_name = 'dbo.sp_site_notifications_insert'
            query = text(
                "call " + create_site_notification_procedure_name + "(:site_id, :notification_id, :status_id, CAST(:email AS character varying), CAST(:user_name AS character varying), CAST(:user_id AS character varying))")
            parameters = {"site_id": notification.site_id, "notification_id": notification.notification_id,
                          "status_id": notification.status_id, "email": notification.email,
                          "user_name": notification.user_name, "user_id": notification.user_id}
            call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        response = {
            "status_code": 200,
            "message": "Created the site notification successfully",
            "data": {}
        }
    except Exception as exc:
           raise exc
    else:
        log.debug("create_site_notification service executed successfully")
        return jsonable_encoder(response)

def update_site_notification(notification: SiteNotification):
    """
    This function is to create notification
    """
    try:
        log.append_keys(service_function="update_site_notification")
        log.debug("Entered into update_site_notification service")
        with db_instance.create_writer_connection() as db:
            update_site_notification_procedure_name = 'dbo.sp_site_notifications_update'
            query = text(
                "call " + update_site_notification_procedure_name + "(:id, :site_id, :notification_id, :status_id, CAST(:email AS character varying), CAST(:user_name AS character varying), CAST(:user_id AS character varying))")
            parameters = {"id": notification.id, "site_id": notification.site_id,
                          "notification_id": notification.notification_id, "status_id": notification.status_id,
                          "email": notification.email, "user_name": notification.user_name,
                          "user_id": notification.user_id}
            call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        response = {
            "status_code": 200,
            "message": "Updated the site notification in Database successfully",
            "data": {}
        }

    except Exception as exc:
        raise exc
    else:
        log.debug("update_contact service executed successfully")
        return jsonable_encoder(response)
   

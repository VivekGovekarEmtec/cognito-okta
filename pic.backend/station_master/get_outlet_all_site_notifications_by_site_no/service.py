from sqlalchemy import text
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.encoder import jsonable_encoder

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service("Station master getOutletAllSiteNotificationsBySiteNo")


def get_notifications_all_by_site_id(site_id: int, language: str):
    """
    This function will return notifications by site id
    """
    try:
        log.append_keys(service_function="get_notifications_all_by_site_id")
        log.debug("Entered into get_notifications_all_by_site_id service")
        with db_instance.create_writer_connection() as db:
            get_outlet_function_name = 'dbo.fn_site_notifications_select_all'
            query = text("SELECT * from " + get_outlet_function_name + "(:site_id, :_lang)")
            parameters = {"site_id": site_id, "_lang": language}
            response_data = call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        if len(response_data) == 0:
            log.debug("No data found in database")

            response = {
                "status_code": 204,
                "message": "No data found in database",
                "data": {}
            }
        else:
            log.debug("Received response from database")
            response = {
                "status_code": 200,
                "message": "Received notification types from Database successfully",
                "data": {"notifications_list_by_site_id": jsonable_encoder(response_data)}
            }
    except Exception as e:
        raise e
    else:
        log.debug("get_notifications_all_by_site_id service executed successfully")
        return response

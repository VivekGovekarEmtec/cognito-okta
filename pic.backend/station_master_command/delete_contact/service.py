from sqlalchemy import text
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
import json
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service("Delete Contact")

def delete_contact(id: int, user_id: str):
    """
    This function will delete contacts from database
    """
    try:
        log.append_keys(service_function="delete_contact")
        log.debug("Entered into delete_contact service")
        with db_instance.create_writer_connection() as db:
            delete_contact_procedure_name = 'dbo.sp_site_contact_method_delete'
            query = text("call " + delete_contact_procedure_name + "( :id,:user_id)")
            parameters = {"id": id, "user_id": user_id}
            call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        response = {
            "status_code": 200,
            "message": "Deleted the contact successfully",
            "data": {}
        }

    except Exception as exc:
        raise exc
    else:
        log.debug("delete_contact service executed successfully")
        return json.loads(json.dumps(response))
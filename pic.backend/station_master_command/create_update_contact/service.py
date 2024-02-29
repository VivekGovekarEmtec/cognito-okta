from sqlalchemy import text
from schemas.contact_schema import Contact #, UpdateContact
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
import json
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service("Station master create/updatecontact")


def create_contact(contact: Contact):
    """
    This api will create contact in database
    """
    try:
        log.append_keys(service_function="create_contact")
        log.debug("Entered into create_contact service")
        with db_instance.create_writer_connection() as db:
            create_contact_procedure_name = 'dbo.sp_site_contact_method_create'
            query = text("call " + create_contact_procedure_name + "( :site_id, :type_id, :value, :user_id)")
            parameters = {"site_id": contact.site_id, "type_id": contact.type_id, "value": contact.value,
                            "user_id": contact.user_id}
            call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        response = {
            "status_code": 200,
            "message": "Created the contact in Database successfully",
            "data": {}
        }

    except Exception as exc:
           raise exc
    else:
        log.debug("create_contact service executed successfully")
        return json.loads(json.dumps(response))


def update_contact(contact: Contact):
    """
    This function will update contacts in database
    """
    try:
        log.append_keys(service_function="update_contact")
        log.debug("Entered into update_contact service")
        with db_instance.create_writer_connection() as db:
            update_contact_procedure_name = 'dbo.sp_site_contact_method_update'
            query = text(
                "call " + update_contact_procedure_name + "( :id,:contact_type_id,CAST(:value AS character varying),CAST(:user_id AS character varying))")
            parameters = {"id": contact.id, "contact_type_id": contact.contact_type_id, "value": contact.value,
                          "user_id": contact.user_id}
            call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        response = {
            "status_code": 200,
            "message": "Updated the contact in Database successfully",
            "data": {}
        }

    except Exception as exc:
        raise exc
    else:
        log.debug("update_contact service executed successfully")
        return json.loads(json.dumps(response))
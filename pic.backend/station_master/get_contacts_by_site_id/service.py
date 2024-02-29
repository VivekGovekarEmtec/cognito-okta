from sqlalchemy import text
import json
from common_component.src.core.helpers.encoder import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log

db_instance = CreateDBConnection()
log = Log().get_logger_service()


def get_contacts_by_site_id(site_id: int, language: str):
    """
    This function will get contact by site id from database
    """
    try:
        log.append_keys(service_function="get_contacts_by_site_id")
        log.debug("Entered into get_contacts_by_site_id service")
        with db_instance.create_writer_connection() as db:
            get_outlet_function_name = 'dbo.fn_site_contact_methods_by_site_id'
            query = text("SELECT * from " + get_outlet_function_name + "( :site_id, :lang)")
            parameters = {"site_id": site_id, "lang": language}
            response_data = call_postgres_function(query=query, parameters=parameters, db=db)
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
                "message": "Received contacts from Database successfully",
                "data": {"contacts_by_site_id_list": response_data}
            }
    except SQLAlchemyError as sql_alchemy_exception:
        raise sql_alchemy_exception

    except Exception as exc:
        raise exc
    else:
        log.debug("get_contacts_by_site_id service executed successfully")
        return jsonable_encoder(response)

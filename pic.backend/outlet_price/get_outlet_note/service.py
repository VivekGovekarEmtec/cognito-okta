from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.helpers.encoder import jsonable_encoder
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service("Get Outlet note")


def get_pricing_note(site_id):
    """
    This API is used to get pricing notes
    """
    try:
        log.append_keys(service_function="get_pricing_note")
        log.debug("Entered into get_pricing_note service")
        with db_instance.create_reader_connection() as db:
            parameters = {"site_id": site_id}
            get_site_notes_function_name = 'dbo.fn_site_note'
            query = text("select * from " + get_site_notes_function_name + '(:site_id)')

            output = call_postgres_function(query=query, parameters=parameters, db=db)
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
                "message": "Received all pricing notes data from Database successfully",
                "data": {"pricing_notes": response_data[0]}
            }
    except Exception as exc:
        raise exc
    else:
        log.debug("get_pricing_note service executed successfully")
        return response

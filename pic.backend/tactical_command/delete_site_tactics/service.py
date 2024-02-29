from sqlalchemy import text

from common_component.src.core.helpers.encoder import jsonable_encoder
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
import json
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service("Delete site tactics")


def delete_site_tactics(id: int):
    """
    This function will delete site tactics from database
    """
    try:
        log.append_keys(service_function="delete_site_tactics")
        log.debug("Entered into delete_site_tactics service")
        with db_instance.create_writer_connection() as db:
            delete_site_tactics_stored_procedure_name = 'dbo.sp_site_tactics_delete'
            parm_dict = {"id": id}
            query = text(
                'CALL ' + delete_site_tactics_stored_procedure_name + '(:id)')
            call_postgres_function(query=query, parameters=parm_dict, db=db)
        log.debug("Received response from database")
        response = {
            "status_code": 200,
            "message": "Deleted site tactics successfully",
            "data": {}
        }

    except Exception as exc:
        raise exc
    else:
        log.debug("delete_site_tactics service executed successfully")
        return jsonable_encoder(response)

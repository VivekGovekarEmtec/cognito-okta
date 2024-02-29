from sqlalchemy import text
import json
from common_component.src.core.helpers.encoder import jsonable_encoder
from temporary_close_schema import TemporaryClose
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log

db_instance = CreateDBConnection()
log = Log().get_logger_service()

def update_temporary_close(temporary_close: TemporaryClose):
    """
    This function is used to update the temporary close time for particular site
    """
    try:
        log.append_keys(service_function="update_temporary_close")
        log.debug("Entered into update_temporary_close service")
        with db_instance.create_writer_connection() as db:
            temporary_close_update_procedure_name = 'dbo.sp_site_temporary_close_update'
            query = text('CALL ' + temporary_close_update_procedure_name +
                         '(:_site_no,:_effective_date,:_expiry_date)')
            parameters = {"_site_no": temporary_close.site_no, "_effective_date": temporary_close.effective_date,
                          "_expiry_date": temporary_close.expiry_date}
            call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        response = {
            "status_code": 200,
            "message": "Updated the temporary close successfully",
            "data": {}
        }
        
    except SQLAlchemyError as sql_alchemy_exception:
        raise sql_alchemy_exception

    except Exception as exc:
        raise exc
    else:
        log.debug("update_temporary_close service executed successfully")
        return jsonable_encoder(response)
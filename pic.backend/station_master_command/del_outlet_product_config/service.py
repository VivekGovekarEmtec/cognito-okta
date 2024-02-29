from sqlalchemy import text
import json
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service()


def delete_outlet_product_configuration(id: int, user_id: str):
    """
    This function is used to delete the site product configuration
    """
    try:
        log.append_keys(service_function="delete_outlet_product_configuration")
        log.debug("Entered into delete_outlet_product_configuration service")
        with db_instance.create_writer_connection() as db:
            delete_product_configuration_procedure_name = 'dbo.sp_site_product_configurations_delete'
            parm_dict = {"id": id, "user_id": user_id}
            query = text(
                'CALL ' + delete_product_configuration_procedure_name + '(:id,:user_id)')
        call_postgres_function(query=query, parameters=parm_dict, db=db)
        log.debug("Received response from database")
        response = {
            "status_code": 200,
            "message": "Deleted the product configuration successfully",
            "data": {}
        }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        return response

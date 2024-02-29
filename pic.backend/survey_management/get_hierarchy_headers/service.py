from sqlalchemy import text
import json
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.encoder import jsonable_encoder      

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service()


def get_hierarchy_header(hierarchy_id: int, language: str, site_id: int):
    """
    This function is used to get the all hierarchy headers and selecting particular hierarchy header by site id and
    hierarchy id
    """
    try:
        log.append_keys(service_function="get_hierarchy_header")
        log.debug("Entered into get_hierarchy_header service")
        with db_instance.create_writer_connection() as db:
            get_hierarchy_header_function_name = "dbo.fn_get_hierarchy_header"
            param_dict = {"hierarchy_id": hierarchy_id, "language": language, "site_id": site_id}
            query = text(
                'SELECT * FROM '
                + get_hierarchy_header_function_name + '(:hierarchy_id,:language,:site_id)')
            output = call_postgres_function(query=query, db=db, parameters=param_dict)
        response_data = jsonable_encoder(output)
        response = {
            "status_code":200,
            "message": "Received hierarchy headers from database successfully",
            "data": response_data
        }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        return response

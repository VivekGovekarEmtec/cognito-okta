from sqlalchemy import text
import json
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.encoder import jsonable_encoder

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service()


def get_competitor_sites_by_site_id_service(site_id: int, language: str):
    """
    This function is used to get the competitor sites data for selected site or outlet
    """
    try:
        log.append_keys(service_function="get_competitor_sites_by_site_id_service")
        log.debug("Entered into get_competitor_sites_by_site_id_service service")
        with db_instance.create_writer_connection() as db:
            get_competitor_sites_by_site_id_function_name = "dbo.fn_competitors_to_survey_by_siteid"
            param_dict = {"site_id": site_id, "language": language}
            query = text(
                'SELECT * FROM '
                + get_competitor_sites_by_site_id_function_name + '(:site_id,:language)')
            output = call_postgres_function(query=query, db=db, parameters=param_dict)
        log.debug("Received response from database")
        response_data = jsonable_encoder(output)
        if output is None :
            response = {
            "status_code":204,
            "message": "Empty result",
            "data": []
        }
        response = {
            "status_code": 200,
            "message": "Received search competitor data from Database successfully",
            "data": {"competitor_sites_by_site_id_list": response_data}
        }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        return response    
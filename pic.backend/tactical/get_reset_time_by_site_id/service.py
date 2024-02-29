from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.helpers.encoder import jsonable_encoder
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log

log = Log().get_logger_service("Get reset time for given site_id")
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()


def get_reset_time_by_site_id(site_id: int):
    """
        This method returns default reset time for given site_id
    """
    try:
        log.append_keys(service_function="get_reset_time_by_site_id")
        log.debug("Entered into get_reset_time_by_site_id service")
        with db_instance.create_reader_connection() as db:
            get_default_reset_time_by_site_id_function_name = 'dbo.fn_site_reset_time'
            query = text("select * from " + get_default_reset_time_by_site_id_function_name + "(:site_id)")
            parameters = {"site_id": site_id}
            output = call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")

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
                "message": "Received default reset time from database successfully",
                "data": {"reset_time": response_data[0]["reset_time"]}
            }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        log.debug("get_reset_time_by_site_id service executed successfully")
        return response

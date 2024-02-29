from sqlalchemy import text
from common_component.src.core.helpers.encoder import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log

db_instance = CreateDBConnection()
log = Log().get_logger_service()


def current_station_time(site_id: int):
    """
    This function is used to get the current station time
    """
    try:
        log.append_keys(service_function="current_station_time")
        log.debug("Entered into current_station_time service")
        param_dict = {
            "site_id": site_id
        }
        with db_instance.create_writer_connection() as db:
            get_time_function_name = 'dbo.fn_current_station_time'
            query = text('SELECT * FROM ' + get_time_function_name + '(:site_id)')
            output = call_postgres_function(query=query, parameters=param_dict, db=db)
        log.debug("Received response from database")
        response_data = jsonable_encoder(output)
        if len(response_data) == 0:
            response = {
                "status_code": 204,
                "message": "station not found",
                "data": None
            }
        else:
            response = {
                "status_code": 200,
                "message": "Received current station time from database successfully",
                "data": response_data[0]
            }

    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception

    except Exception as exc:
        raise exc
    else:
        log.debug("current_station_time service executed successfully")
        return response

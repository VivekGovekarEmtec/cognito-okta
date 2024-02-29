from datetime import datetime
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.helpers.encoder import jsonable_encoder
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log

log = Log().get_logger_service("is site tactic time overlap")
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()


def is_site_tactic_time_overlap(site_id: int, follow_action_id: int, id: int, start_time_new: str, end_time_new: str):
    """
        This method returns if time overlaps
    """
    try:
        log.append_keys(service_function="is_site_tactic_time_overlap")
        log.debug("Entered into is_site_tactic_time_overlap service")
        with db_instance.create_writer_connection() as db:
            parameters = {"site_id": site_id, "follow_action_id": follow_action_id, "id": id}
            get_default_reset_time_by_site_id_function_name = 'dbo.fn_site_tactic_time_validation_details'
            query = text(
                "select * from " + get_default_reset_time_by_site_id_function_name + "(:site_id, :follow_action_id, :id)")
            output = call_postgres_function(query=query, parameters=parameters, db=db)

        log.debug("Received response from database")
        response_data = jsonable_encoder(output)
        time_overlap = False

        timestamp_start_time = datetime.strptime(start_time_new, '%H:%M').timestamp()
        timestamp_end_time = datetime.strptime(end_time_new, '%H:%M').timestamp()

        if len(response_data) == 0:
            time_overlap = False
        else:
            for item in response_data:
                start_time = datetime.strptime(item['start_time'], '%H:%M').timestamp()
                end_time = datetime.strptime(item['end_time'], '%H:%M').timestamp()
                time_overlap = (timestamp_start_time <= end_time) and (start_time <= timestamp_end_time)
                if time_overlap:
                    break
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
                "data": {"is_time_overlap": time_overlap}
            }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        log.debug("is_site_tactic_time_overlap service executed successfully")
        return response

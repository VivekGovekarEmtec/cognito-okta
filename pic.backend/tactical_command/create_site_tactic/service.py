from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.helpers.encoder import jsonable_encoder
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from schema import SiteTacticInsert

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service("Insert site tactic")


def create_site_tactics(site_tactic_insert: SiteTacticInsert):
    """
    This function will add site tactic
    """
    try:
        log.append_keys(service_function="create_site_tactics")
        log.debug("Entered into create_site_tactics service")
        with db_instance.create_writer_connection() as db:
            create_site_tactics_procedure_name = "dbo.sp_site_tactics_insert"
            param_dict = {
                "site_id": site_tactic_insert.site_id,
                "follow_action_id": site_tactic_insert.follow_action_id,
                "follow_movement_id": site_tactic_insert.follow_movement_id,
                "movement_option_id": site_tactic_insert.movement_option_id,
                "cpl_tolerance": site_tactic_insert.cpl_tolerance,
                "rack_fwd_tolerance": site_tactic_insert.rack_fwd_tolerance,
                "follow_options": site_tactic_insert.follow_options,
                "last_updated_user_id": site_tactic_insert.last_updated_user_id,
                "comments": site_tactic_insert.comments[:8000],
                "start_time": site_tactic_insert.start_time,
                "end_time": site_tactic_insert.end_time,
                "follow_sites": site_tactic_insert.follow_sites
            }
            query = text(
                'CALL '
                + create_site_tactics_procedure_name +
                '(:site_id,'
                ':follow_action_id,'
                ':follow_movement_id,'
                ':movement_option_id,'
                ':cpl_tolerance,'
                ':rack_fwd_tolerance,'
                ':follow_options,'
                ':last_updated_user_id,'
                ':comments,'
                ':start_time,'
                ':end_time,'
                ':follow_sites)')
            call_postgres_function(query=query, db=db, parameters=param_dict)
        log.debug("Received response from database")
        response = {
            "status_code": 200,
            "message": "New site tactics created successfully",
            "data": {}
        }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        log.debug("create_site_tactics service executed successfully")
        return jsonable_encoder(response)
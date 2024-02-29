from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.encoder import jsonable_encoder
from schema import SiteTacticUpdate

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service("update site tactics")


def update_site_tactics(site_tactic_update: SiteTacticUpdate):
    """
    This function is used to save the regulated prices adjustment for site
    """
    try:
        log.append_keys(service_function="update_regulated_prices_adjustment")
        log.debug("Entered into update_regulated_prices_adjustment service")
        with db_instance.create_writer_connection() as db:
            update_site_tactics_procedure_name = "dbo.sp_site_tactics_update"
            param_dict = {
                "id": site_tactic_update.id,
                "follow_action_id": site_tactic_update.follow_action_id,
                "follow_movement_id": site_tactic_update.follow_movement_id,
                "movement_option_id": site_tactic_update.movement_option_id,
                "cpl_tolerance": site_tactic_update.cpl_tolerance,
                "rack_fwd_tolerance": site_tactic_update.rack_fwd_tolerance,
                "follow_options": site_tactic_update.follow_options,
                "last_updated_user_id": site_tactic_update.last_updated_user_id,
                "comments": site_tactic_update.comments[:8000],
                "start_time": site_tactic_update.start_time,
                "end_time": site_tactic_update.end_time,
                "follow_sites": site_tactic_update.follow_sites
            }
            query = text(
                'CALL '
                + update_site_tactics_procedure_name +
                '(:id,'
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
                "message": "Updated site tactic successfully",
                "data": {}
            }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        return jsonable_encoder(response)
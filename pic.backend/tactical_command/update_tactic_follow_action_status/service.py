from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.encoder import jsonable_encoder

log = Log().get_logger_service("tactic_follow_action_status_update")
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()


def update_action_status(tactic_follow_action_status_update):
    """
        This function is used to update tactics follow action status
    """
    try:
        log.append_keys(service_function="update_action_status")
        log.debug("Entered into update_action_status service")
        with db_instance.create_writer_connection() as db:
            update_tactic_follow_action_status_procedure_name = "dbo.sp_tactic_follow_action_status_Update"
            param_dict = {
                "site_id": tactic_follow_action_status_update.site_id,
                "follow_action_id": tactic_follow_action_status_update.follow_action_id,
                "status_id": tactic_follow_action_status_update.status_id
            }
            query = text(
                'CALL '
                + update_tactic_follow_action_status_procedure_name +
                '(:site_id,'
                ':follow_action_id,'
                ':status_id)')
            call_postgres_function(query=query, db=db, parameters=param_dict)
        log.debug("Received response from database")
        response = {
            "status_code": 200,
            "message": "Updated the tactic follow action status successfully",
            "data": {}
        }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        log.debug("update_action_status service executed successfully")
        return jsonable_encoder(response)
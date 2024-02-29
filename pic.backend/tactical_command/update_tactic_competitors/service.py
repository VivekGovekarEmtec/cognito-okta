import json
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from schema import UpdateTacticCompetitorsForOutlets
from common_component.src.core.helpers.encoder import jsonable_encoder

log = Log().get_logger_service("update tactic competitors for outlets")
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()


def update_tactic_competitors_for_outlets(add_tactic_competitors: UpdateTacticCompetitorsForOutlets):
    """
        This function is used to update_tactic_competitors_for_outlets
    """
    try:
        log.append_keys(service_function="update_tactic_competitors_for_outlets")
        log.debug("Entered into update_tactic_competitors_for_outlets service")
        with db_instance.create_writer_connection() as db:
            update_competitor_for_outlets_procedure_name = 'dbo.sp_delete_and_insert_tactic_competitor_for_outlets'

            json_parse = json.loads(add_tactic_competitors.json())
            json_data = str(json_parse['comp_list_json']).replace("'", '"')

            query = text(
                "call " + update_competitor_for_outlets_procedure_name + "(CAST(:site_id AS integer), CAST(:user_id "
                                                                         "AS character varying), CAST(:comp_list_json"
                                                                         " AS jsonb))")
            parameters = {"site_id": add_tactic_competitors.site_id,
                          "user_id": add_tactic_competitors.user_id,
                          "comp_list_json": json_data}
            call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        response = {
            "status_code": 200,
            "message": "updated competitors successfully",
            "data": {}
        }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        log.debug("update_tactic_competitors_for_outlets service executed successfully")
        return jsonable_encoder(response)

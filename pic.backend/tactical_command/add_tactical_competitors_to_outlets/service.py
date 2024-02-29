import json
from sqlalchemy import text
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from sqlalchemy.exc import SQLAlchemyError

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service("Add tactical competitors to outlets")


def add_tactic_competitors_for_outlets(add_tactic_competitors):
    """
    This function will add tactic competitors for outlet
    """
    try:
        log.append_keys(service_function="add_tactic_competitors_for_outlets")
        log.debug("Entered into add_tactic_competitors_for_outlets service")
        with db_instance.create_writer_connection() as db:
            add_competitor_for_outlets_procedure_name = 'dbo.sp_tactic_competitor_insert'
            val = json.loads(add_tactic_competitors.json())
            json_data = str(val['json_data']).replace("'", '"')

            query = text(
                "call " + add_competitor_for_outlets_procedure_name + "(CAST(:json_data AS character varying), CAST("
                                                                      ":user_id AS character varying))")
            parameters = {"json_data": json_data,
                          "user_id": add_tactic_competitors.user_id}
            call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        response = {
            "status_code": 200,
            "message": "added new tactic competitors successfully",
            "data": {}
        }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        log.debug("add_tactic_competitors_for_outlets service executed successfully")
        return response

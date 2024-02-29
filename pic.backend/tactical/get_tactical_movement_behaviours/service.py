from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.helpers.encoder import jsonable_encoder
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service("Get Tactical Movement Behaviours")


def get_tactical_movement_behaviours(lang: str):
    """
    This API is used to get tactical movement behaviours
    """
    try:
        log.append_keys(service_function="get_tactical_movement_behaviours")
        log.debug("Entered into get_tactical_movement_behaviours service")
        with db_instance.create_reader_connection() as db:
            parameters = {"lang": lang}
            get_tactical_movement_function_name = 'dbo.fn_tactic_movement_behaviours'
            query = text("select * from " + get_tactical_movement_function_name + '(cast(:lang AS character varying))')
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
                "message": "Received tactical movement behaviours data from database successfully",
                "data": {
                    "behaviours": response_data
                }
        }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        log.debug("get_tactical_movement_behaviours service executed successfully")
        return response

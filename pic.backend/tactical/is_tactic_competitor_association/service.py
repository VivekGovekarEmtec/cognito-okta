from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.helpers.encoder import jsonable_encoder
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log

log = Log().get_logger_service("is tactical competitor associated")
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()


def is_tactical_competitor_associated(site_id: int, kent_id: int):
    """
    This returns true if tactic is associated with given competitor
    """
    try:
        log.append_keys(service_function="is_tactical_competitor_associated")
        log.debug("Entered into is_tactical_competitor_associated service")
        with db_instance.create_reader_connection() as db:
            is_tactic_competitor_associated_function_name = 'dbo.fn_is_tactic_competitor_associated_validation'
            query = text("select * from " + is_tactic_competitor_associated_function_name + "(:site_id, :kent_id)")
            parameters = {"site_id": site_id, "kent_id": kent_id}
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
                "message": "Received is_tactical_competitor_associated data from database successfully",
                "data": {"is_association_exists": response_data[0]["is_association_exists"]}
            }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        log.debug("is_tactical_competitor_associated service executed successfully")
        return response

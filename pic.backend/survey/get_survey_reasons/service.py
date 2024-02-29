from sqlalchemy import text
import json
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.encoder import jsonable_encoder

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service()


def get_survey_reasons(language: str):
    """
    This function is used to return survey reasons data
    """
    try:
        with db_instance.create_writer_connection() as db:
            get_survey_reasons_function_name = 'dbo.fn_survey_reasons'
            query = text("SELECT * from " + get_survey_reasons_function_name + "(:language)")
            parameters = {"language": language}
            output = call_postgres_function(query=query, parameters=parameters, db=db)
        response_data =jsonable_encoder(output)
        response = {
            "status_code": 200,
            "message": "survey reasons",
            "data": response_data
        }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        return response_data

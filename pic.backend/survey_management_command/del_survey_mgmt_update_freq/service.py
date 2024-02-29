from sqlalchemy import text
import json
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service()


def delete_survey_management(survey_ids: str,user_id:str):
    try:
        log.append_keys(service_function="delete_survey_management")
        log.debug("Entered into delete_survey_management service")
        with db_instance.create_writer_connection() as db:
            delete_survey_management_frequency_procedure_name = "dbo.sp_survey_management_frequency_delete"
            param_dict = {
             "survey_ids": survey_ids,
             "user_id":user_id
            }
            query = text('CALL ' + delete_survey_management_frequency_procedure_name +
                         '(:survey_ids,:user_id)')
            call_postgres_function(query=query, db=db, parameters=param_dict)
        log.debug("Received response from database")
        response = {
            "status_code": 200,
            "message": "Deleted the survey management frequencies successfully",
            "data": {}
        }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        return response

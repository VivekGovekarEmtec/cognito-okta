from sqlalchemy import text
import json
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from schemas.survey_management_schema import CreateSurveyManagement

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service()


def create_survey_management(survey_manage: CreateSurveyManagement):
    """
        This function is used to create survey management frequency
    """
    try:
        log.append_keys(service_function="create_survey_management")
        log.debug("Entered into create_survey_management service")
        with db_instance.create_writer_connection() as db:
            create_survey_management_procedure_name = "dbo.sp_survey_management_insert"
            param_dict = {
                "site_id": survey_manage.site_id,
                "kent_id": survey_manage.kent_id,
                "product_id": survey_manage.product_id,
                "new_frequency": survey_manage.new_frequency,
                "effective_date": survey_manage.effective_date,
                "expiry_date": survey_manage.expiry_date,
                "from_1": survey_manage.from_1,
                "from_2": survey_manage.from_2,
                "to_1": survey_manage.to_1,
                "to_2": survey_manage.to_2,
                "from_3": survey_manage.from_3,
                "to_3": survey_manage.to_3,
                "from_4": survey_manage.from_4,
                "to_4": survey_manage.to_4,
                "from_5": survey_manage.from_5,
                "to_5": survey_manage.to_5,
                "user": survey_manage.user
            }
            query = text(
                'CALL '
                + create_survey_management_procedure_name +
                '(:site_id,'
                ':kent_id,'
                ':product_id,'
                ':new_frequency,'
                ':effective_date,'
                ':expiry_date,'
                ':from_1,'
                ':to_1,'
                ':from_2,'
                ':to_2,'
                ':from_3,'
                ':to_3,'
                ':from_4,'
                ':to_4,'
                ':from_5,'
                ':to_5,'
                ':user)')
            call_postgres_function(query=query, db=db, parameters=param_dict)
        log.debug("Received response from database")
        response = {
            "status_code": 200,
            "message": "Saved the survey management frequencies successfully",
            "data": {}
        }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        return response

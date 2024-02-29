from sqlalchemy import text
import json
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from schemas.survey_management_schema import UpdateSurveyManagement
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service()


def update_survey_management(survey_manage: UpdateSurveyManagement):
    """
           This function is used update survey management frequency
    """
    try:
        log.append_keys(service_function="update_survey_management")
        log.debug("Entered into update_survey_management service")
        with db_instance.create_writer_connection() as db:
            update_survey_management_procedure_name = "dbo.sp_survey_management_update"
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
                "user": survey_manage.user,
                "row_identifiers": survey_manage.rows_identifiers
            }
            query = text(
                'CALL '
                + update_survey_management_procedure_name +
                '(:site_id,'
                'CAST(:kent_id AS character varying),'
                ':product_id,'
                'CAST(:new_frequency AS character varying),'
                ':effective_date,'
                'CAST(:row_identifiers AS character varying),'
                ':expiry_date,'
                'CAST(:from_1 AS character varying),'
                'CAST(:to_1 AS character varying),'
                'CAST(:from_2 AS character varying),'
                'CAST(:to_2 AS character varying),'
                'CAST(:from_3 AS character varying),'
                'CAST(:to_3 AS character varying),'
                'CAST(:from_4 AS character varying),'
                'CAST(:to_4 AS character varying),'
                'CAST(:from_5 AS character varying),'
                'CAST(:to_5 AS character varying),'
                'CASt(:user AS character varying))')

            call_postgres_function(query=query, db=db, parameters=param_dict)
        log.debug("Received response from database")
        response = {
            "status_code": 200,
            "message": "Updated the survey management frequencies successfully",
            "data": {}
        }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        return response

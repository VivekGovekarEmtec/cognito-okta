from sqlalchemy import text
import json
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from datetime import datetime
from common_component.src.core.helpers.encoder import jsonable_encoder

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service()


def survey_management_frequency_exist(site_id: int, kent_id: str, product_id: int, frequency: str,
                                      effective_date: datetime):
    """
    This function is used to check if already frequency any frequency is there for particular site id and kent id's
    """
    try:
        log.append_keys(service_function="survey_management_frequency_exist")
        log.debug("Entered into survey_management_frequency_exist service")
        with db_instance.create_writer_connection() as db:
            check_survey_management_frequency_exist_function_name = "dbo.fn_survey_management_frequency_id_exists"
            param_dict = {
                "site_id": site_id,
                "kent_id": kent_id,
                "product_id": product_id,
                "frequency": frequency,
                "effective_date": effective_date
            }
            query = text(
                'SELECT * FROM '
                + check_survey_management_frequency_exist_function_name +
                '(:site_id,'
                'CAST(:kent_id AS character varying),'
                ':product_id,'
                'CAST(:frequency AS character varying),'
                'CAST(:effective_date AS timestamp without time zone))')

            output = call_postgres_function(query=query, db=db, parameters=param_dict)
        log.debug("Received response from database")
        response_data = jsonable_encoder(output)
        response = {
            "status_code": 200,
            "message": "Received the frequency status from database successfully",
            "data": response_data
        }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        return response
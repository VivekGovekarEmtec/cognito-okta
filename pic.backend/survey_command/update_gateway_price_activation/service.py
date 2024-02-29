from sqlalchemy import text
import json
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from gateway_survey_activation_schema import PriceActivation

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service()


def update_price_survey_activation(price_activation: PriceActivation):
    try:
        log.append_keys(service_function="update_price_survey_activation")
        log.debug("Entered into update_price_survey_activation service")
        with db_instance.create_writer_connection() as db:
            update_price_survey_activation_procedure_name = "gateway.sp_price_survey_activation_update"
            param_dict = {"status": price_activation.status, "user_id": price_activation.user_id}
            query = text('CALL ' + update_price_survey_activation_procedure_name +
                         '(:status,:user_id)')
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

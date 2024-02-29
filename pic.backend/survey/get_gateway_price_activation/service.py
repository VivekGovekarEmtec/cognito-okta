from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.encoder import jsonable_encoder


db_instance = CreateDBConnection()
log = Log().get_logger_service()


def get_price_survey_activation():
    """
    This function is used to get all unreviewed surveys
    """
    try:
        with db_instance.create_writer_connection() as db:
            price_survey_activation_function_name = "gateway.fn_price_survey_activation"
            query = text('SELECT * FROM ' + price_survey_activation_function_name +
                         '()')
            output = call_postgres_function(query=query, db=db)
            
        log.debug("Received response from database")
        response_data = jsonable_encoder(output)
        
        if not response_data:
            response = {
            "status_code":204,
            "message": "Data not found in the database",
            "data": None
        }
        else:
            response = {
                "status_code": 200,
                "message": "Got the gateway price activation status successfully",
                "data": {"gateway_price_activation": response_data[0]}
            }

        
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        return response

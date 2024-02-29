from sqlalchemy import text
import json
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.encoder import jsonable_encoder

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service()


def get_price_compliance_banner():
    """
     This function is used to get price compliance banner
    """
    try:
        with db_instance.create_writer_connection() as db:
            get_price_compliance_function_name = "dbo.fn_price_compliance_available"
            query = text(
                'SELECT * FROM '
                + get_price_compliance_function_name +
                '()')
            output = call_postgres_function(query=query, db=db)
        response_data = jsonable_encoder(output)
        if not response_data:
            response = {
                "status_code": 204,
                "message": "Price compliance status is not found.",
                "data": response_data
            }
        else:
            response = {
                "status_code": 200,
                "message": "Received the price compliance status from database successfully",
                "data": response_data
            }
       
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        return response

from sqlalchemy import text
import json
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.encoder import jsonable_encoder

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service()


def get_regulated_prices_pending_banner(language: str, user_id: str):
    """
        This function is used to get regulated prices pending authorization banner
    """
    try:
        with db_instance.create_writer_connection() as db:
            get_regulated_prices_pending_authorization_function_name = "dbo.fn_regulated_prices_pending_authorization"
            param_dict = {
                "language": language,
                "user_id": user_id
            }
            query = text(
                'SELECT * FROM '
                + get_regulated_prices_pending_authorization_function_name +
                '(:language,:user_id)')
            output = call_postgres_function(query=query, db=db, parameters=param_dict)
        response_data = jsonable_encoder(output)
        if not response_data:
            response = {
                "status_code":204,
                "message": "Regulated pending prices status is not found.",
                "data": None
            }
        else:
             response = {
                "status_code": 200,
                "message": "Received the regulated prices pending authorization from database successfully",
                "data": {"regulated_pending_prices": response_data}
            }
        
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        return response

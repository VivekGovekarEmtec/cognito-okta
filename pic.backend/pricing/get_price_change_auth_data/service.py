from sqlalchemy import text
from common_component.src.core.helpers.encoder import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log


log = Log().get_logger_service("Get Cancel Price")
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()


# price change auth
def get_price_change_auth_data(user_id: str, lang: str):
    """
    This API is used to get price change authorization information
    """
    try:
        log.append_keys(service_function="get_price_change_auth_data")
        log.debug("Entered into get_price_change_auth_data service")
        with db_instance.create_writer_connection() as db:
            get_function_name = 'dbo.fn_product_price_changes_to_notify_select'
            query = text(
                "SELECT * from " + get_function_name + "(CAST(:user_id AS character varying), CAST(:lang AS character varying))")
            parameters = {"user_id": user_id, 'lang': lang}

            output = call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        response_data = jsonable_encoder(output)

        response = {
            "status_code": 200,
            "message": "get the price change authorization information successfully",
            "data": {"price_change_auth_data": response_data}
        }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        log.debug("get_price_change_auth_data service executed successfully")
        return response

from sqlalchemy import text
from common_component.src.core.helpers.encoder import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log


log = Log().get_logger_service("Get Cancel Price")
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()


def get_price_change_cancel_data(lang: str):
    """
    This API is used to get price change cancel information
    """
    try:
        log.append_keys(service_function="get_price_change_cancel_data")
        log.debug("Entered into get_price_change_cancel_data service")
        with db_instance.create_reader_connection() as db:
            get_function_name = 'dbo.fn_get_price_changes_to_cancel'
            query = text(
                "SELECT * from " + get_function_name + "(CAST(:lang AS character varying), :change_id, "
                                                       ":price_change_type)")
            parameters = {'lang': lang, 'change_id': None, "price_change_type": None}

            output = call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        response_data = jsonable_encoder(output)

        response = {
            "status_code": 200,
            "message": "get the price change cancel information successfully",
            "data": {"cancel_price_change_list": response_data}
        }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        log.debug("get_price_change_cancel_data service executed successfully")
        return response

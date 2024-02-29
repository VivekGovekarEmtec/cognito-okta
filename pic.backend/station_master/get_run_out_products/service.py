from sqlalchemy import text
from common_component.src.core.helpers.encoder import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log

db_instance = CreateDBConnection()
log = Log().get_logger_service()


def get_run_out_products(language: str):
    """
    This function is used to get alternative product
    """
    try:
        log.append_keys(service_function="get_run_out_products")
        log.debug("Entered into get_run_out_products service")
        with db_instance.create_writer_connection() as db:
            run_out_product_function_name = 'dbo.fn_run_out_product'
            param_dict = {"language": language}
            query = text(
                'SELECT * FROM ' + run_out_product_function_name +
                '(:language)')
            output = call_postgres_function(query=query, db=db, parameters=param_dict)
        log.debug("Received response from database")
        response_data = jsonable_encoder(output)
        if len(response_data) == 0:
            response = {
                "status_code": 204,
                "message": "Data not found in the database",
                "data": None
            }
        else:
            response = {
                "status_code": 200,
                "message": "Received run out products from database successfully",
                "data": {"run_out_products": response_data}
            }

    except SQLAlchemyError as sql_alchemy_exception:
        raise sql_alchemy_exception

    except Exception as exc:
        raise exc
    else:
        log.debug("get_run_out_products service executed successfully")
        return response

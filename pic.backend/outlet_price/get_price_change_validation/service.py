from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.encoder import jsonable_encoder

log = Log().get_logger_service("Get regulated prize details service")
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()


# reset price change
def valid_price_change(site_id, product_id, price, site_list, is_request_now, request_date):
    """
    This function is used to check if any price change with existing site id is present or not
    """
    try:
        log.append_keys(service_function="valid_price_change")
        log.debug("Entered into valid_price_change service")
        with db_instance.create_writer_connection() as db:
            valid_price_change_function_name = 'dbo.fn_site_product_price_changes_validation'
            parameters = {
                "site_id": site_id,
                "product_id": product_id,
                "price": price,
                "site_list": site_list,
                "is_request_now": is_request_now,
                "request_date": request_date
            }
            query = text(
                'SELECT * FROM ' + valid_price_change_function_name +
                '(:site_id,'
                ':product_id,'
                ':price,'
                'CAST(:site_list AS character varying),'
                ':is_request_now,'
                'CAST(:request_date AS timestamp without time zone))'
            )
            output = call_postgres_function(query, parameters, db)
        log.debug("Received response from database")
        response_data = jsonable_encoder(output)
        if len(response_data) == 0:
            response = {
                "status_code": 204,
                "message": "Data not found in the database",
                "data": None
            }
        else:
            if isinstance(response_data, list) and len(response_data) == 1:
                response_data = response_data[0]
            response = {
                "status_code": 200,
                "message": "Received price change validation from Database successfully",
                "data": response_data
            }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        log.info("valid_price_change service executed successfully")
        return response

from sqlalchemy import text
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.encoder import jsonable_encoder
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service("outlet price getSiteProducts")


def get_pme_products(site_id: int, language: str):
    """
    This function is used to get the site products with pme value
    """
    try:
        log.append_keys(service_function="get_pme_products")
        log.debug("Entered into get_pme_products service")
        with db_instance.create_writer_connection() as db:
            pme_product_function_name = "dbo.fn_site_products"
            param_dict = {
                "site_id": site_id,
                "language": language
            }
            query = text(
                'SELECT * FROM ' + pme_product_function_name + '(:site_id,CAST(:language AS character varying))'
            )
            output = call_postgres_function(query=query, parameters=param_dict, db=db)
        log.debug("Received response from database")
        response_data = jsonable_encoder(output)
        if len(response_data) != 0:
            response_data = response_data

            response = {
                "status_code": 200,
                "message": "Received site products with pme calculation from database successfully",
                "data": {"products": response_data}
            }
        else:
            response = {
                "status_code": 204,
                "message": "No data found in database",
                "data": {}
            }
    except Exception as exc:
        raise exc
    else:
        log.debug("get_pme_products service executed successfully")
        return response
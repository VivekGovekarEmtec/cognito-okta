import json
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from schema import PriceChangeDeleteList
from common_component.src.core.helpers.encoder import jsonable_encoder

log = Log().get_logger_service("Create price on hold")
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()


def delete_price_change(priceChangeDeleteList: PriceChangeDeleteList):
    """
    This API is used to delete price change sites
    """
    try:
        log.append_keys(service_function="delete_price_change")
        log.debug("Entered into delete_price_change service")
        priceChangeDeleteListJson = json.loads(priceChangeDeleteList.json())
        json_data = str(priceChangeDeleteListJson['json_data']).replace("'", '"')

        with db_instance.create_writer_connection() as db:
            get_procedure_name = 'dbo.sp_site_product_price_changes_json_delete'
            query = text(
                "call " + get_procedure_name + "(CAST(:json AS character varying), CAST(:user_id AS character varying))")
            parameters = {"json": json_data, 'user_id': priceChangeDeleteListJson['user_id']}

            output = call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        response_data = jsonable_encoder(output)

        response = {
            "status_code": 200,
            "message": "deleted the price change information successfully",
            "data": {}
        }

    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        log.debug("delete_price_change service executed successfully")
        return response


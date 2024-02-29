from sqlalchemy import text
import json
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from schema import PriceOnHoldInsertList
from common_component.src.core.helpers.encoder import jsonable_encoder

log = Log().get_logger_service("Insert price on hold")
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()


def site_price_on_hold_json_insert(priceOnHoldInsertList: PriceOnHoldInsertList):
    """
    This API is used to insert multiple price on hold using json
    """
    try:
        log.append_keys(service_function="site_price_on_hold_json_insert")
        log.debug("Entered into site_price_on_hold_json_insert service")
        with db_instance.create_writer_connection() as db:
            get_procedure_name = 'dbo.sp_site_price_on_hold_json_insert'
            val = json.loads(priceOnHoldInsertList.json())
            json_data = str(val['json_data']).replace("'", '"')
            query = text(
                "CALL " + get_procedure_name + "(CAST(:json_data AS character varying), CAST(:user_id AS character varying), CAST(:notes AS character varying))")
            parameters = {"json_data": json_data, 'user_id': priceOnHoldInsertList.user_id,
                          'notes': priceOnHoldInsertList.notes}
            output = call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        response_data = jsonable_encoder(output)

        # response needs to be updated
        response = {
            "status_code": 200,
            "message": "inserted price on hold successfully",
            "data": {}
        }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        log.debug("site_price_on_hold_json_insert service executed successfully")
        return response

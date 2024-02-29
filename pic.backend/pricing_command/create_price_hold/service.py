from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from schema import CreatePriceOnHold
from common_component.src.core.helpers.encoder import jsonable_encoder

log = Log().get_logger_service("Create price on hold")
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()


def insert_price_hold(price_hold: CreatePriceOnHold):
    """
    This function is used to call the stored procedure for saving price on hold data
    """
    try:
        log.append_keys(service_function="insert_price_hold")
        log.debug("Entered into insert_price_hold service")
        with db_instance.create_writer_connection() as db:
            price_hold_procedure_name = 'dbo.sp_site_price_on_hold_insert'
            parameters = {
                "site_id": price_hold.site_id,
                "product_id": price_hold.product_id,
                "effective_date": price_hold.effective_date,
                "expiry_date": price_hold.expiry_date,
                "user_id": price_hold.user_id,
                "note": price_hold.note
            }
            query = text(
                'CALL ' + price_hold_procedure_name +
                '(CAST(:site_id AS character varying),'
                ':product_id,'
                'CAST(:effective_date AS timestamp without time zone),'
                'CAST(:expiry_date AS timestamp without time zone),'
                'CAST(:user_id AS character varying),'
                'CAST(:note AS character varying))'
            )
            call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        response = {
            "status_code": 200,
            "message": "Saved price on hold data successfully",
            "data": {}
        }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as e:
        raise e
    else:
        log.debug("insert_price_hold service executed successfully")
        return jsonable_encoder(response)

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from schema import PriceOnHoldUpdate
from common_component.src.core.helpers.encoder import jsonable_encoder

log = Log().get_logger_service("Update Price on hold")
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()


def site_price_on_hold_by_site_id_update(priceOnHoldUpdate: PriceOnHoldUpdate):
    """
    This API is used to update price on hold by site id
    """
    try:
        log.append_keys(service_function="site_price_on_hold_by_site_id_update")
        log.debug("Entered into site_price_on_hold_by_site_id_update service")
        with db_instance.create_writer_connection() as db:
            get_function_name = 'dbo.sp_site_price_on_hold_by_site_id_update'
            query = text(
                "CALL " + get_function_name + "(:site_no, :product_id, CAST(:effective_date AS timestamp without time zone), CAST(:expiry_date AS timestamp without time zone),  CAST(:user_id AS character varying), CAST(:notes AS character varying))")
            parameters = {"site_no": priceOnHoldUpdate.site_no, 'product_id': priceOnHoldUpdate.product_id,
                          'effective_date': priceOnHoldUpdate.effective_date,
                          'expiry_date': priceOnHoldUpdate.expiry_date, 'user_id': priceOnHoldUpdate.user_id,
                          'notes': priceOnHoldUpdate.notes}
            output = call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        response_data = jsonable_encoder(output)

        # response needs to be updated
        response = {
            "status_code": 200,
            "message": "updated price on hold successfully",
            "data": {}
        }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        log.debug("site_price_on_hold_by_site_id_update service executed successfully")
        return response


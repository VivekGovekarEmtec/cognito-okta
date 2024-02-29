from sqlalchemy import text
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.encoder import jsonable_encoder

log = Log().get_logger_service("Delete price on hold")
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()


def site_price_on_hold_by_site_id_delete(site_no: int, product_id: int, user_current_date: datetime, user_id: str):
    """
    This API is used to delete price on hold by site id
    """
    try:
        log.append_keys(service_function="site_price_on_hold_by_site_id_delete")
        log.debug("Entered into site_price_on_hold_by_site_id_delete service")
        with db_instance.create_writer_connection() as db:
            get_function_name = 'dbo.sp_site_price_on_hold_by_site_id_delete'
            query = text(
                "CALL " + get_function_name + "(:site_no, :product_id, CAST(:user_current_date AS timestamp without time zone),  CAST(:user_id AS character varying))")
            parameters = {"site_no": site_no, 'product_id': product_id, 'user_current_date': user_current_date,
                          'user_id': user_id}
            output = call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        jsonable_encoder(output)

        # response needs to be updated
        response = {
            "status_code": 200,
            "message": "deleted price on hold successfully",
            "data": {}
        }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        log.debug("site_price_on_hold_by_site_id_delete service executed successfully")
        return response


from sqlalchemy import text
import json
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from regulated_price_schema import RegulatePriceSchema
from common_component.src.core.helpers.encoder import jsonable_encoder

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service()

def update_regulated_prices_adjustment(regulated_price: RegulatePriceSchema):
    """
    This function is used to save the regulated prices adjustment for site
    """
    try:
        log.append_keys(service_function="update_regulated_prices_adjustment")
        log.debug("Entered into update_regulated_prices_adjustment service")
        with db_instance.create_writer_connection() as db:
            update_regulated_price_adjustment_procedure_name = 'dbo.sp_regulated_prices_adjustment_insert'
            query = text('CALL ' + update_regulated_price_adjustment_procedure_name +
                         '(:site_no,'
                         ':zone_id,'
                         ':gas_full_serve_adjustment,'
                         ':diesel_full_serve_adjustment,'
                         ':gas_adjustment,'
                         ':diesel_adjustment,'
                         'CAST(:user_id AS character varying),'
                         ':id)')
            parameters = {
                "site_no": regulated_price.site_no,
                "zone_id": regulated_price.zone_id,
                "gas_full_serve_adjustment": regulated_price.gas_full_serve_adjustment,
                "diesel_full_serve_adjustment": regulated_price.diesel_full_serve_adjustment,
                "gas_adjustment": regulated_price.gas_adjustment,
                "diesel_adjustment": regulated_price.diesel_adjustment,
                "user_id": regulated_price.user_id,
                "id": regulated_price.id
            }
            call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        response = {
            "status_code": 200,
            "message": "Saved the regulated price adjustment successfully",
            "data": {}
        }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        return jsonable_encoder(response)
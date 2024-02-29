from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from schema import NBApplyPricing
from common_component.src.core.helpers.encoder import jsonable_encoder

log = Log().get_logger_service("Create price on hold")
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()


def apply_pricing_nb(nb_apply: NBApplyPricing):
    """
    This service function is used to apply the regulated prices of new brunswick
    """
    try:
        log.append_keys(service_function="apply_pricing_nb")
        log.debug("Entered into apply_pricing_nb service")
        with db_instance.create_writer_connection() as db:
            created_auth_no = None
            created_fright_date = None
            regulated_price_type_id: int = 1
            parameters = {
                'regulated_price_type_id': regulated_price_type_id,
                'effective_date': nb_apply.effective_date,
                'ref_date_1': nb_apply.ref_date_1,
                'ref_date_2': nb_apply.ref_date_2,
                'regular_retail_price': nb_apply.regular_retail_price,
                'regular_retail_with_delivery_price': nb_apply.regular_retail_with_delivery_price,
                'regular_full_serve_with_delivery_price': nb_apply.regular_full_serve_with_delivery_price,
                'regular_to_plus_diff': nb_apply.regular_to_plus_diff,
                'plus_retail_price': nb_apply.plus_retail_price,
                'plus_retail_with_delivery_price': nb_apply.plus_retail_with_delivery_price,
                'plus_full_serve_with_delivery_price': nb_apply.plus_full_serve_with_delivery_price,
                'regular_to_supreme_diff': nb_apply.regular_to_supreme_diff,
                'supreme_retail_price': nb_apply.supreme_retail_price,
                'supreme_retail_with_delivery_price': nb_apply.supreme_retail_with_delivery_price,
                'supreme_full_serve_with_delivery_price': nb_apply.supreme_full_serve_with_delivery_price,
                'diesel_retail_price': nb_apply.diesel_retail_price,
                'diesel_retail_with_delivery_price': nb_apply.diesel_retail_with_delivery_price,
                'diesel_full_serve_with_delivery_price': nb_apply.diesel_full_serve_with_delivery_price,
                'inserted_user_id': nb_apply.inserted_user_id,
                'auth_number': nb_apply.auth_number,
                'auth_no': created_auth_no,
                'fright_date': created_fright_date
            }
            nb_apply_procedure_name = 'dbo.sp_regulated_prices_header_nb_insert'
            query = text(
                'CALL ' + nb_apply_procedure_name +
                '(:regulated_price_type_id,'
                'CAST(:effective_date AS timestamp without time zone),'
                'CAST(:ref_date_1 AS timestamp without time zone),'
                'CAST(:ref_date_2 AS timestamp without time zone),'
                ':regular_retail_price,'
                ':regular_retail_with_delivery_price,'
                ':regular_full_serve_with_delivery_price,'
                ':regular_to_plus_diff,'
                ':plus_retail_price,'
                ':plus_retail_with_delivery_price,'
                ':plus_full_serve_with_delivery_price,'
                ':regular_to_supreme_diff,'
                ':supreme_retail_price,'
                ':supreme_retail_with_delivery_price,'
                ':supreme_full_serve_with_delivery_price,'
                ':diesel_retail_price,'
                ':diesel_retail_with_delivery_price,'
                ':diesel_full_serve_with_delivery_price,'
                'CAST(:inserted_user_id AS character varying),'
                'CAST(:auth_no AS character varying),'
                'CAST(:fright_date AS timestamp without time zone),'
                ':auth_number)'
            )
            output = call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        response_data = output.mappings().all()

        response = {
            "status_code": 200,
            "message": "Applied regulated prices for new brunswick",
            "data": response_data[0]
        }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        log.debug("apply_pricing_nb service executed successfully")
        return jsonable_encoder(response)

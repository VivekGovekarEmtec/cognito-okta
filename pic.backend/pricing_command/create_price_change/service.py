from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.helpers.price_helper import convert_to_dpl
from common_component.src.core.helpers.ssm_helper import get_ssm_parameter
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from schema import CreatePriceChange
from common_component.src.core.helpers.encoder import jsonable_encoder

log = Log().get_logger_service("Create price on hold")
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()


def insert_price_change(price_change: CreatePriceChange):
    """
    This function is used to create price change request
    """
    try:
        log.append_keys(service_function="insert_price_change")
        log.debug("Entered into insert_price_change service")
        max_diff_param = get_ssm_parameter('/pic/pricing/max_diff_price', True)
        with db_instance.create_writer_connection() as db:
            price_change_procedure_name = 'dbo.sp_site_product_price_changes_insert'
            parameters = {
                "site_id": price_change.site_id,
                "product_id": price_change.product_id,
                "request_date": price_change.request_date,
                "request_price": convert_to_dpl(price_change.request_price),
                "comment": price_change.comment,
                "move_with": price_change.move_with,
                "hierarchy_header_id": price_change.hierarchy_header_id,
                "site_list": price_change.site_list,
                "over_write_notification_type_with": price_change.over_write_notification_type_with,
                "max_diff_price": max_diff_param,
                "user_id": price_change.user_id,
                "is_auto_authorization": price_change.is_auto_authorization,
                "is_request_now": price_change.is_request_now
            }
            query = text(
                'CALL ' + price_change_procedure_name +
                '(:site_id,'
                ':product_id,'
                'CAST(:request_date AS timestamp without time zone),'
                ':request_price,'
                ':comment,'
                ':move_with,'
                ':hierarchy_header_id,'
                ':site_list,'
                ':over_write_notification_type_with,'
                ':max_diff_price,'
                ':user_id,'
                ':is_auto_authorization,'
                ':is_request_now)'
            )
            call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        response = {
            "status_code": 200,
            "message": "Saved price change request in Database successfully",
            "data": {}
        }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as e:
        raise e
    else:
        log.debug("insert_price_change service executed successfully")
        return jsonable_encoder(response)

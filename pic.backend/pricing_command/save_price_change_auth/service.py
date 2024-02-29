from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from schema import SiteProductPriceChangeUpdate
from common_component.src.core.helpers.encoder import jsonable_encoder

log = Log().get_logger_service("Create price on hold")
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()


def price_change_auth_update(siteProductPriceChangeUpdate: SiteProductPriceChangeUpdate):
    """
    This API is used to update price change authorization information
    """
    try:
        log.append_keys(service_function="price_change_auth_update")
        log.debug("Entered into price_change_auth_update service")
        with db_instance.create_writer_connection() as db:
            get_procedure_name = 'dbo.sp_site_product_price_changes_update'
            query = text(
                "call " + get_procedure_name + "(:product_price_change_id,:site_id,:product_id,: is_request_now,CAST(:request_date AS timestamp without time zone),CAST(:request_prices AS decimal), CAST(:autho_no AS character varying), CAST(:comment AS character varying),:kent_id,:hierarchy_header_id,CAST(:site_list AS character varying),:over_write_notification_type_with,CAST(:user_id AS character varying),:price_change_status)")
            parameters = {"product_price_change_id": siteProductPriceChangeUpdate.product_price_change_id,
                          'site_id': siteProductPriceChangeUpdate.site_id,
                          'product_id': siteProductPriceChangeUpdate.product_id,
                          'is_request_now': siteProductPriceChangeUpdate.is_request_now,
                          'request_date': siteProductPriceChangeUpdate.request_date,
                          'request_prices': siteProductPriceChangeUpdate.request_prices,
                          'autho_no': siteProductPriceChangeUpdate.autho_no,
                          'comment': siteProductPriceChangeUpdate.comment,
                          'kent_id': siteProductPriceChangeUpdate.kent_id,
                          'hierarchy_header_id': siteProductPriceChangeUpdate.hierarchy_header_id,
                          'site_list': siteProductPriceChangeUpdate.site_list,
                          'over_write_notification_type_with': siteProductPriceChangeUpdate.over_write_notification_type_with,
                          'user_id': siteProductPriceChangeUpdate.user_id,
                          'price_change_status': siteProductPriceChangeUpdate.price_change_status}

            output = call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        response_data = jsonable_encoder(output)

        response = {
            "status_code": 200,
            "message": "get the price change authorization information successfully",
            "data": response_data
        }

    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        log.debug("price_change_auth_update service executed successfully")
        return response


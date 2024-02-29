from sqlalchemy import text
import json
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.price_helper import convert_to_dpl
from product_schema import UpdateSiteProductConfig

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service()


def update_outlet_product_configuration(id: int, product_config: UpdateSiteProductConfig):
    """ 
     This function is used to update the site product configuration
    """
    try:
        log.append_keys(service_function="update_outlet_product_configuration")
        log.debug("Entered into update_outlet_product_configuration service")
        with db_instance.create_writer_connection() as db:
            update_product_config_procedure_name = 'dbo.sp_site_product_configuration_update'
            param_dict = {
                "id": id,
                "site_id": product_config.site_id,
                "product_id": product_config.product_id,
                "run_out_product_id": product_config.run_out_product_id,
                "base_difference_price": convert_to_dpl(product_config.base_difference_price),
                "fs_difference_price": convert_to_dpl(product_config.fs_difference_price),
                "notification_type_code": product_config.notification_type_code,
                "is_temp_not_available": product_config.is_temp_not_available,
                "effective_date": product_config.effective_date,
                "expiry_date": product_config.expiry_date,
                "pos_product_grade": product_config.pos_product_grade,
                "user_id": product_config.updated_by_user_id,
                "regulated_prices_reference_value_id": product_config.regulated_prices_reference_value_id
            }
            query = text(
                'CALL ' + update_product_config_procedure_name +
                '(:id,'
                ':site_id,:product_id,'
                ':run_out_product_id,'
                ':base_difference_price,'
                ':fs_difference_price,'
                ':notification_type_code,'
                'CAST(:is_temp_not_available AS smallint),'
                ':effective_date,'
                ':expiry_date,'
                'CAST(:pos_product_grade AS character varying),'
                'CAST(:user_id AS character varying),'
                ':regulated_prices_reference_value_id)')
            call_postgres_function(query=query, parameters=param_dict, db=db)
        log.debug("Received response from database")
        response = {
            "status_code": 200,
            "message": "Update product configuration successfully",
            "data": {}
        }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        return response

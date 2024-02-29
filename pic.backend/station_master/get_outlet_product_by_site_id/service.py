from sqlalchemy import text
from common_component.src.core.helpers.encoder import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from decimal import Decimal

db_instance = CreateDBConnection()
log = Log().get_logger_service()


def convert_to_cpl(price: Decimal):
    """
    This function is used to convert price into CPL
    """
    return price * 100


def modify_product_response(data):
    modified_result = []
    for i in data:
        response_dict = {
            'id': i.id,
            'site_id': i.site_id,
            'product_id': i.product_id,
            'product_code': i.product_code,
            'product_name': i.product_name,
            'base_difference_price': convert_to_cpl(i.base_difference_price),
            'fs_difference_price': convert_to_cpl(i.fs_difference_price),
            'promotion_adjustment': i.promotion_adjustment,
            'notification_type_code': i.notification_type_code,
            'notification_type': i.notification_type,
            'is_temp_not_available': i.is_temp_not_available,
            'effective_date': i.effective_date,
            'expiry_date': i.expiry_date,
            'pos_product_grade': i.pos_product_grade,
            'run_out_product_id': i.run_out_product_id,
            'regulated_prices_value_id': i.regulated_prices_value_id
        }
        modified_result.append(response_dict)
    log.debug("modify_product_response service executed successfully")
    return modified_result


def get_outlet_product_configuration_by_site_no(site_id: int, language: str):
    """
    This function is used to get the product configuration using site no
    """
    try:
        log.append_keys(service_function="get_outlet_product_configuration_by_site_no")
        log.debug("Entered into get_outlet_product_configuration_by_site_no service")
        with db_instance.create_writer_connection() as db:
            get_outlet_product_by_site_no_function_name = "dbo.fn_site_product_configuration_by_site_id"
            param_dict = {"site_id": site_id, "language": language}
            query = text(
                'SELECT * FROM '
                + get_outlet_product_by_site_no_function_name + '(:site_id,:language)')
            data = call_postgres_function(query=query, db=db, parameters=param_dict)
            output = modify_product_response(data)
        log.debug("Received response from database")
        response_data = jsonable_encoder(output)
        if len(response_data) == 0:
            response = {
                "status_code": 204,
                "message": "Data not found in the database",
                "data": None
            }
        else:
            response = {
                "status_code": 200,
                "message": "Received products configuration from database successfully",
                "data": {"outlet_product_configuration_by_site_no": response_data}
            }

    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception

    except Exception as exc:
        raise exc
    else:
        log.debug("get_outlet_product_configuration_by_site_no service executed successfully")
        return response

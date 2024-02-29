from decimal import Decimal
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.helpers.encoder import jsonable_encoder
from common_component.src.core.helpers.price_helper import convert_to_dpl
from common_component.src.core.helpers.ssm_helper import get_ssm_parameter
from common_component.src.core.repositories.data_repository import CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_services.services.outlet_service import get_outlet_price

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service("get valid price diff")


def get_valid_price_diff(site_id: int, requested_price: Decimal, product_id: int, lang: str):
    """
    This function is used to validate the requested price with maximum price diff i.e 0.040 dpl
    """
    try:
        log.append_keys(service_function="get_valid_price_diff")
        log.debug("Entered into get_valid_price_diff service")
        req_price = Decimal(convert_to_dpl(requested_price))
        max_diff_param = get_ssm_parameter('/pic/pricing/max_diff_price', True)
        max_diff_price = Decimal(max_diff_param)

        actual_price = get_outlet_price(site_id=site_id, lang=lang)
        actual_price_str = '0.00'
        actual_product_price = Decimal(actual_price_str)
        match product_id:
            # supreme
            case 1:
                if actual_price['price']['supreme_ss_value'] is not None:
                    actual_product_price = Decimal(
                        actual_price['price']['supreme_ss_value'])
                else:
                    response = {
                        "status_code": 204,
                        "message": "Data not found in the database",
                        "data": None
                    }
                    return response
            # regular
            case 2:
                if actual_price['price']['reg_ss_value'] is not None:
                    actual_product_price = Decimal(
                        actual_price['price']['reg_ss_value'])
                else:
                    response = {
                        "status_code": 204,
                        "message": "Data not found in the database",
                        "data": None
                    }
                    return response
            # plus
            case 3:
                if actual_price['price']['plus_ss_value'] is not None:
                    actual_product_price = Decimal(
                        actual_price['price']['plus_ss_value'])
                else:
                    response = {
                        "status_code": 204,
                        "message": "Data not found in the database",
                        "data": None
                    }
                    return response

            # diesel
            case 4:
                if actual_price['price']['diesel_ss_value'] is not None:
                    actual_product_price = Decimal(
                        actual_price['price']['diesel_ss_value'])
                else:
                    response = {
                        "status_code": 204,
                        "message": "Data not found in the database",
                        "data": None
                    }
                    return response
            # regular +
            case 7:
                if actual_price['price']['plus_ss_value'] is not None:
                    actual_product_price = Decimal(
                        actual_price['price']['plus_ss_value'])
                else:
                    response = {
                        "status_code": 204,
                        "message": "Data not found in the database",
                        "data": None
                    }
                    return response
            # supreme +
            case 8:
                if actual_price['price']['supreme_plus_ss_value'] is not None:
                    actual_product_price = Decimal(
                        actual_price['price']['supreme_plus_ss_value'])
                else:
                    response = {
                        "status_code": 204,
                        "message": "Data not found in the database",
                        "data": None
                    }
                    return response

        if actual_product_price == 0:
            return actual_product_price

        response_data = True
        if abs(actual_product_price - req_price) < max_diff_price:
            response_data = False
        response = {
            "status_code": 200,
            "message": "Received price valid difference",
            "data": {
                'max_diff_value': max_diff_price,
                'is_diff_greater_than_max': response_data
            }
        }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        log.debug("get_valid_price_diff service executed successfully")
        return jsonable_encoder(response)


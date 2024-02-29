from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.encoder import jsonable_encoder
from common_services.services import outlet_service

log = Log().get_logger_service("Get regulated prize details service")
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()


# reset price change
def get_outlet_current_price(site_id, lang):
    """
    This API is used to get prices
    """
    try:
        log.append_keys(service_function="get_outlet_current_price")
        log.debug("Entered into get_outlet_current_price service")
        with db_instance.create_writer_connection() as db:
            # Get data for margins
            parameters = {"site_id": site_id}
            get_price_function_name = 'dbo.fn_site_details_for_current_outlet_price'
            query = text("select * from " +
                         get_price_function_name + '(:site_id)')
            output = call_postgres_function(
                query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        response_data = jsonable_encoder(output)

        if isinstance(response_data, list) and len(response_data) == 1:
            response_data = response_data[0]

        price_common = {
            "status_code": 200,
            "message": "Received price data from Database successfully",
            "data": jsonable_encoder(response_data)
        }

        price_result = outlet_service.get_outlet_price(site_id, lang)
        if price_common["data"] == [] or price_result["price"] == []:
            response = {
                "status_code": 204,
                "message": "Data not found in the database",
                "data": None
            }
        else:
            price_common["data"].update(price_result)

            # Create a new dictionary with the same structure
            price_common["data"] = {
                "site_id": price_common["data"]["site_id"],
                "address": price_common["data"]["address"],
                "brand_marketer": price_common["data"]["brand_marketer"],
                "city": price_common["data"]["city"],
                "price": {
                    "source_type": price_common["data"]["price"]["source_type"],
                    "effective_date": price_common["data"]["price"]["ss_effective_date"],
                    "reg_ss_value": price_common["data"]["price"]["reg_ss_value"],
                    "reg_fs_value": price_common["data"]["price"]["reg_fs_value"],
                    "reg_prev_ss_value": price_common["data"]["price"]["reg_prev_ss_value"],
                    "reg_prev_effective_date": price_common["data"]["price"]["reg_prev_effective_date"],
                    "prev_reg_user_name": price_common["data"]["price"]["previous_reg_user_name"],
                    "plus_ss_value": price_common["data"]["price"]["plus_ss_value"],
                    "plus_fs_value": price_common["data"]["price"]["plus_fs_value"],
                    "supreme_ss_value": price_common["data"]["price"]["supreme_ss_value"],
                    "supreme_fs_value": price_common["data"]["price"]["supreme_fs_value"],
                    "supreme_plus_ss_value": price_common["data"]["price"]["supreme_plus_ss_value"],
                    "supreme_plus_fs_value": price_common["data"]["price"]["supreme_plus_fs_value"],
                    "diesel_ss_value": price_common["data"]["price"]["diesel_ss_value"],
                    "diesel_fs_value": price_common["data"]["price"]["diesel_fs_value"],
                    "diesel_prev_ss_value": price_common["data"]["price"]["diesel_prev_ss_value"],
                    "diesel_prev_effective_date": price_common["data"]["price"]["diesel_prev_effective_date"],
                    "prev_diesel_user_name": price_common["data"]["price"]["previous_diesel_user_name"],
                    "diesel_effective_date": price_common["data"]["price"]["diesel_effective_date"],
                    "diesel_user_name": price_common["data"]["price"]["diesel_user_name"],
                    "display_order": price_common["data"]["price"]["display_order"],
                    "volume": price_common["data"]["price"]["volume"]
                }
            }

            response = price_common
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        log.debug("get_outlet_current_price service executed successfully -> %s", response)
        print(response)
        return response

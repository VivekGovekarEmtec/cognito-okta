import json
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from schema import SiteProductPriceChange
from common_component.src.core.helpers.encoder import jsonable_encoder

log = Log().get_logger_service("Reset price change")
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()


def validation(siteProductPriceValidation: SiteProductPriceChange):
    """
    This API is used to validate price change for multiple sites
    """
    try:
        log.append_keys(service_function="validation")
        log.debug("Entered into validation service")
        siteProductPriceChangeJson = json.loads(siteProductPriceValidation.json())
        for obj in siteProductPriceChangeJson['outlet_data']:
            obj['product_id'] = siteProductPriceChangeJson['product_id']
            obj['price'] = siteProductPriceChangeJson['price']

        json_data = str(siteProductPriceChangeJson['outlet_data']).replace("'", '"')

        with db_instance.create_writer_connection() as db:
            get_function_name = 'dbo.fn_site_product_price_changes_json_validation'
            query = text(
                "SELECT * from " + get_function_name + "(CAST(:json AS character varying), CAST(:site_list AS character varying), :is_request_now, CAST(:request_date AS timestamp without time zone), :product_id)")
            parameters = {"json": json_data, 'site_list': None, 'is_request_now': 0, 'request_date': None,
                          'product_id': None, 'price': 0}

        output = call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        response_data = jsonable_encoder(output)

        response = {
            "status_code": 200,
            "message": "get the station information successfully",
            "data": response_data
        }

    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as e:
        raise e
    else:
        log.debug("save_note service executed successfully")
        return jsonable_encoder(response)


def save_price_change(siteProductPriceChange: SiteProductPriceChange):
    """
    This API is used to save price change for multiple sites
    """
    try:
        log.append_keys(service_function="save_price_change")
        log.debug("Entered into save_price_change service")
        siteProductPriceChangeJson = json.loads(siteProductPriceChange.json())
        for obj in siteProductPriceChangeJson['outlet_data']:
            obj['product_id'] = siteProductPriceChangeJson['product_id']
            obj['price'] = siteProductPriceChangeJson['price']

        json_data = str(siteProductPriceChangeJson['outlet_data']).replace("'", '"')

        with db_instance.create_writer_connection() as db:
            get_procedure_name = 'dbo.sp_site_product_price_changes_json_insert'
            query = text(
                "call " + get_procedure_name + "(CAST(:json AS character varying),:price_change_type_code, CAST(:user_id AS character varying))")
            parameters = {"json": json_data, 'price_change_type_code': 1,
                          'user_id': siteProductPriceChangeJson['user_id']}

            output = call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        response_data = jsonable_encoder(output)

        response = {
            "status_code": 200,
            "message": "save the price changes successfully",
            "data": {}
        }

    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        log.debug("save_price_change service executed successfully")
        return response

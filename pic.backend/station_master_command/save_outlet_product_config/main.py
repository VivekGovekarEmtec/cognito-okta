from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import get_query_param_value, create_response
from common_component.src.core.handlers.exception_handler import sqlalchemy_exception_handler, unhandled_exception_handler
from service import update_outlet_product_configuration
from product_schema import UpdateSiteProductConfig
from aws_lambda_powertools.utilities.parser import parse

log = Log().get_logger_service("Save Update Outlet Product Configuration")


@log.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    """
        This function used to update the existing site product configuration
    """
    log.info("Entered into event handler")
    log.set_correlation_id(context.aws_request_id)
    log.append_keys(log_stream=context.log_stream_name)
    try:
        log.append_keys(resource_path="/master/product/saveUpdateOutletProductConfiguration/{id}")
        log.debug("Entered into update_outlet_product_configuration Router")
        path_string_params = event["pathParameters"]
        id = get_query_param_value(path_string_params, "id", int)
        request = event['body']
        parsed_payload: UpdateSiteProductConfig = parse(event=request, model=UpdateSiteProductConfig)
        update_product = update_outlet_product_configuration(id, parsed_payload)
        print("****update_product****", update_product)
        log.debug("Received response from update_outlet_product_configuration Service")
    except SQLAlchemyError as sae:
            # Catch and handle SQLAlchemy errors
        result = sqlalchemy_exception_handler(sae)
        return create_response(result)
    except Exception as exc:
            # Catch and handle Unhandled errors
        result = unhandled_exception_handler(exc)
        return create_response(result)
    else:
        return create_response(update_product)
    
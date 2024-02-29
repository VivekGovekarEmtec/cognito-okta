from sqlalchemy.exc import SQLAlchemyError
from service import get_outlet_configuration_by_site_id
from common_services.services.outlet_service import get_outlet_detail_by_site_id
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import create_response, get_query_param_value
from common_component.src.core.handlers.exception_handler import sqlalchemy_exception_handler, \
    unhandled_exception_handler

log = Log().get_logger_service("Station master GetOutletDetailsByOutletNo")


@log.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    log.debug("Entered into Get OutletDetailsByOutletNo handler")
    log.set_correlation_id(context.aws_request_id)
    log.append_keys(log_stream=context.log_stream_name)
    log.append_keys(resource_path=event['path'])
    try:
        query_string_params = event["queryStringParameters"]
        site_id = get_query_param_value(query_string_params, "site_id", int)
        language = get_query_param_value(query_string_params, "language", str)
        user_id = get_query_param_value(query_string_params, "user_id", str)
        user_id = user_id or ''
        outlet_by_id_result = get_outlet_detail_by_site_id(site_id, language, user_id)
        log.debug("Received response from get_outlet_detail_by_site_id Service")

        if not outlet_by_id_result:
            result = _get_no_response(f"No data found for site {site_id}")
        #        Below code is to get data for outlet configurations
        outlet_configuration_by_site_id_result = get_outlet_configuration_by_site_id(site_id)
        if not outlet_configuration_by_site_id_result:
            result = _get_no_response(f"No configuration data found for site {site_id}")

        outlet_by_id_result.update(outlet_configuration_by_site_id_result)
        log.debug("Received response from GetQoutletDetailsByOutletNo Service")

        result = {
            "status_code": 200,
            "message": "Received outlet detail by site number data from Database successfully",
            "data": {'outlet_detail_by_site_no': outlet_by_id_result}
        }
    except SQLAlchemyError as sae:
        # Catch and handle SQLAlchemy errors
        print("error is -> ", sae)
        result = sqlalchemy_exception_handler(sae)
        return create_response(result)
    except Exception as exc:
        # Catch and handle Unhandled errors
        result = unhandled_exception_handler(exc)
        return create_response(result)
    else:
        return create_response(result)


def _get_no_response(message: str):
    return {
        "status_code": 204,
        "message": message,
        "data": {}
    }
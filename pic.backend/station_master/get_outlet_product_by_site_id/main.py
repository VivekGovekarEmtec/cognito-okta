from service import get_outlet_product_configuration_by_site_no
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import get_query_param_value, create_response
from common_component.src.core.handlers.exception_handler import sqlalchemy_exception_handler, \
    unhandled_exception_handler

log = Log().get_logger_service("Get pic-national-station-master-lambda-getOutletProductBySiteId")


@log.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    log.info("Entered into event handler")
    log.set_correlation_id(context.aws_request_id)
    log.append_keys(log_stream=context.log_stream_name)
    log.append_keys(resource_path=event['path'])
    try:
        query_string_params = event["queryStringParameters"]
        site_id = get_query_param_value(query_string_params, "site_id", int)
        language = get_query_param_value(query_string_params, "language", str)
        response_data = get_outlet_product_configuration_by_site_no(site_id, language)

    except SQLAlchemyError as sae:
        print(str(sae), 'sql error')
        result = sqlalchemy_exception_handler(sae)
        return create_response(result)
    except Exception as exc:
        print(str(exc), 'unhandled error')
        result = unhandled_exception_handler(exc)
        return create_response(result)
    else:
        return create_response(response_data)

from service import get_all_regulated_reference_values
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import create_response
from common_component.src.core.handlers.exception_handler import sqlalchemy_exception_handler, \
    unhandled_exception_handler

log = Log().get_logger_service("Get pic-national-station-master-lambda-getReferenceValueTypes")


@log.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    log.info("Entered into event handler")
    log.set_correlation_id(context.aws_request_id)
    log.append_keys(log_stream=context.log_stream_name)
    log.append_keys(resource_path=event['path'])
    try:
        response_data = get_all_regulated_reference_values()

    except SQLAlchemyError as sae:
        result = sqlalchemy_exception_handler(sae)
        return create_response(result)
    except Exception as exc:
        result = unhandled_exception_handler(exc)
        return create_response(result)
    else:
        return create_response(response_data)

from sqlalchemy.exc import SQLAlchemyError
from service import is_photo_required_toggle
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import create_response, get_query_param_value
from common_component.src.core.handlers.exception_handler import sqlalchemy_exception_handler, unhandled_exception_handler

log = Log().get_logger_service("Get pic-national-station-master-command-lambda-saveNewOutletProductConfiguration")

@log.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    log.info("Entered into event handler")
    log.set_correlation_id(context.aws_request_id)
    log.append_keys(log_stream=context.log_stream_name)
    log.append_keys(resource_path=event['path'])
    try:
        query_string_params = event["queryStringParameters"]
        site_no = get_query_param_value(query_string_params, "site_no", int)
        user_id = get_query_param_value(query_string_params, "user_id", str)
        if(event['path'] == "/competitors/association/isPhotoRequiredToggle"):
            is_photo_toggle_response = is_photo_required_toggle(site_no, user_id=user_id)
        else: 
            is_photo_toggle_response = {
            "status_code": 404,
            "message": "Invalid api",
            "data": {}
        }
        log.debug("Received response from isPhotoRequiredToggle service")
    
    except SQLAlchemyError as sae:
        # Catch and handle SQLAlchemy errors
        result = sqlalchemy_exception_handler(sae)
        return create_response(result)
    except Exception as exc:
        # Catch and handle Unhandled errors
        result = unhandled_exception_handler(exc)
        return create_response(result)
    else:
        return create_response(is_photo_toggle_response)
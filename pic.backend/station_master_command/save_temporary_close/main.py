from sqlalchemy.exc import SQLAlchemyError
from service import update_temporary_close
from common_component.src.core.utils.Logger import Log
from temporary_close_schema import TemporaryClose
from aws_lambda_powertools.utilities.parser import parse
from common_component.src.core.helpers.helper import create_response
from common_component.src.core.handlers.exception_handler import sqlalchemy_exception_handler, unhandled_exception_handler

log = Log().get_logger_service("Get pic-national-station-master-command-lambda-saveTemporaryClose")

@log.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    log.info("Entered into event handler")
    log.set_correlation_id(context.aws_request_id)
    log.append_keys(log_stream=context.log_stream_name)
    log.append_keys(resource_path=event['path'])
    try:
        request = event['body']
        parsed_payload: TemporaryClose = parse(event=request,model=TemporaryClose)
        if(event['path'] == "/master/temporaryClose/saveTemporaryClose"):
            temporary_close_result = update_temporary_close(parsed_payload)
        else: 
            temporary_close_result = {
            "status_code": 404,
            "message": "Invalid api",
            "data": {}
        }
        log.debug("Received response from update_temporary_close Service")
    
    except SQLAlchemyError as sae:
        # Catch and handle SQLAlchemy errors
        result = sqlalchemy_exception_handler(sae)
        return create_response(result)
    except Exception as exc:
        # Catch and handle Unhandled errors
        result = unhandled_exception_handler(exc)
        return create_response(result)
    else:
        return create_response(temporary_close_result)
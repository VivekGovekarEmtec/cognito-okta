from sqlalchemy.exc import SQLAlchemyError
from service import create_competitor
from common_component.src.core.utils.Logger import Log
from manage_schema import CreateCompetitor
from aws_lambda_powertools.utilities.parser import parse
from common_component.src.core.helpers.helper import create_response
from common_component.src.core.handlers.exception_handler import sqlalchemy_exception_handler, unhandled_exception_handler

log = Log().get_logger_service("Get pic-national-competitor-command-lambda-createNewCompetitors")

@log.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    log.info("Entered into event handler")
    log.set_correlation_id(context.aws_request_id)
    log.append_keys(log_stream=context.log_stream_name)
    log.append_keys(resource_path=event['path'])
    try:
        request = event['body']
        parsed_payload: CreateCompetitor = parse(event=request,model=CreateCompetitor)
        if(event['path'] == "/competitors/manage/createNewCompetitors"):
            create_competitor_response = create_competitor(parsed_payload)
        else: 
            create_competitor_response = {
            "status_code": 404,
            "message": "Invalid api",
            "data": {}
        }
        log.debug("Received response from create_competitor Service")
    
    except SQLAlchemyError as sae:
        # Catch and handle SQLAlchemy errors
        result = sqlalchemy_exception_handler(sae)
        return create_response(result)
    except Exception as exc:
        # Catch and handle Unhandled errors
        result = unhandled_exception_handler(exc)
        return create_response(result)
    else:
        return create_response(create_competitor_response)
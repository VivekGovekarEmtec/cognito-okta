from sqlalchemy.exc import SQLAlchemyError
from aws_lambda_powertools.utilities.typing import LambdaContext
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import get_query_param_value, create_response
from common_component.src.core.handlers.exception_handler import sqlalchemy_exception_handler, unhandled_exception_handler
from service import create_site_notification,update_site_notification
from schemas.notification_schema import SiteNotification
from aws_lambda_powertools.utilities.parser import ValidationError, parse

log = Log().get_logger_service("Get all unreviewed survey")


@log.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    log.info("Entered into notification Router")
    log.set_correlation_id(context.aws_request_id)
    log.append_keys(log_stream=context.log_stream_name)
    log.append_keys(resource_path=event['path'])
    try:
        request = event["body"]
        #log.append_keys(resource_path="/master/contact/createNewContact")
        parsed_payload: SiteNotification = parse(event=request, model=SiteNotification)
        if(event['httpMethod'] == 'POST'):
            create_notification_response = create_site_notification(parsed_payload)
        elif(event['httpMethod'] == 'PUT'):
            create_notification_response = update_site_notification(parsed_payload)
        else: 
            create_notification_response = {
            "status_code": 404,
            "message": "Invalid api",
            "data": {}
        }
        log.debug("Received response from contact Service")

    except SQLAlchemyError as sae:
        # Catch and handle SQLAlchemy errors
        result = sqlalchemy_exception_handler(sae)
        return create_response(result)
    except Exception as exc:
        # Catch and handle Unhandled errors
        result = unhandled_exception_handler(exc)
        return create_response(result)
    else:
        return create_response(create_notification_response)
    
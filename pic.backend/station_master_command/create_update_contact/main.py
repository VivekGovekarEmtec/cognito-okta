from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import create_response
from common_component.src.core.handlers.exception_handler import sqlalchemy_exception_handler, unhandled_exception_handler
from schemas.contact_schema import Contact
from aws_lambda_powertools.utilities.parser import parse
from service import create_contact, update_contact
import os
log = Log().get_logger_service("Create Update Contact")


@log.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    log.info("Entered into create_contactevent handler")
    log.set_correlation_id(context.aws_request_id)
    log.append_keys(log_stream=context.log_stream_name)
    log.append_keys(resource_path=event['path'])
    try:
        request = event["body"]
        parsed_payload: Contact = parse(event=request, model=Contact)
        create_contact_path = '/master/contact/createNewContact' #os.environ.get('CREATE_CONTACT_ROUTE')
        update_contact_path = '/master/contact/updateContact' #os.environ.get('UPDATE_CONTACT_ROUTE')
        if(event['path'] == create_contact_path):
            create_contact_response = create_contact(parsed_payload)
        elif(event['path'] == update_contact_path):
            create_contact_response = update_contact(parsed_payload)
        else: 
            create_contact_response = {
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
        return create_response(create_contact_response)

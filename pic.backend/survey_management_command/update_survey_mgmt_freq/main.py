
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import get_query_param_value, create_response
from common_component.src.core.handlers.exception_handler import sqlalchemy_exception_handler, unhandled_exception_handler
from service import update_survey_management
from schemas.survey_management_schema import UpdateSurveyManagement
from aws_lambda_powertools.utilities.parser import parse

log = Log().get_logger_service("Update Survey Management")


@log.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    log.info("Entered into event handler")
    log.set_correlation_id(context.aws_request_id)
    log.append_keys(log_stream=context.log_stream_name)
    try:
        log.append_keys(resource_path="/competitors/surveyManagement/updateSurveyManagementFrequency")
        log.debug("Entered into update_survey_management_frequency Router")
        request = event['body']
        parsed_payload: UpdateSurveyManagement = parse(request, model=UpdateSurveyManagement)
        response_data = update_survey_management(parsed_payload)
    except SQLAlchemyError as sae:
        # Catch and handle SQLAlchemy errors
        result = sqlalchemy_exception_handler(sae)
        return create_response(result)
    except Exception as exc:
        # Catch and handle Unhandled errors
        result = unhandled_exception_handler(exc)
        return create_response(result)
    else:
        return create_response(response_data)

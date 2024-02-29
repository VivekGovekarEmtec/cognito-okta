from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import  create_response
from common_component.src.core.handlers.exception_handler import sqlalchemy_exception_handler, unhandled_exception_handler
from aws_lambda_powertools.utilities.parser import parse
from service import send_pdf_using_email
from schemas.survey_scheduel_schema import StationReportList


log = Log().get_logger_service("Create Survey Management Frequency")


@log.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    log.info("Entered into event handler")
    log.set_correlation_id(context.aws_request_id)
    log.append_keys(log_stream=context.log_stream_name)
    """
        This router function is used to send pdf using email
    """
    try:
        log.append_keys(resource_path="/common/competitors/surveyScheduleDetail/sendStationReport")
        log.debug("Entered into get_survey_schedule_detail Router")
        request = event['body']
        parsed_payload: StationReportList = parse(request, model=StationReportList)
        get_header_text = send_pdf_using_email(parsed_payload)
        log.debug("Received response from send_pdf_using_email Service")
    except SQLAlchemyError as sae:
        # Catch and handle SQLAlchemy errors
        result = sqlalchemy_exception_handler(sae)
        return create_response(result)
    except Exception as exc:
        # Catch and handle Unhandled errors
        result = unhandled_exception_handler(exc)
        return create_response(result)
    else:
        return create_response(get_header_text)

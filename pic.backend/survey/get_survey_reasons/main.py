from service import get_survey_reasons
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import get_query_param_value, create_response
from common_component.src.core.handlers.exception_handler import sqlalchemy_exception_handler, unhandled_exception_handler

log = Log().get_logger_service("Get Survey Reasons")


@log.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    log.info("Entered into event handler")
    log.set_correlation_id(context.aws_request_id)
    log.append_keys(log_stream=context.log_stream_name)
    if event['path'] == "/common/competitors/surveys/getSurveyReasons":
        try:
            query_string_params = event["queryStringParameters"]
            language = get_query_param_value(query_string_params, "language", str)
            response_data = get_survey_reasons(language)

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

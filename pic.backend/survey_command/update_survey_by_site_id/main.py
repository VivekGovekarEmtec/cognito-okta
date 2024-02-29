from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import get_query_param_value, create_response
from common_component.src.core.handlers.exception_handler import sqlalchemy_exception_handler, unhandled_exception_handler
from service import update_competitor_sites_by_site_id_service
from survey_schema import UpdateCompetitorSites
from aws_lambda_powertools.utilities.parser import parse

log = Log().get_logger_service("Update Survey By SiteId")
@log.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    log.info("Entered into event handler")
    log.set_correlation_id(context.aws_request_id)
    log.append_keys(log_stream=context.log_stream_name)
    """
        This is the router function used to delete survey management frequency
    """
    try:
        """
        This api will update existing competitor by site id
        """
        log.append_keys(resource_path="/competitors/surveys/updateSurveyBySiteId")
        log.debug("Entered into update_competitor_by_site_id Router")
        request = event['body']
        parsed_payload: UpdateCompetitorSites = parse(request, model=UpdateCompetitorSites)
        price_activation_status_update = update_competitor_sites_by_site_id_service(parsed_payload)
        log.debug("Received response from update_competitor_sites_by_site_id_service Service")
    except SQLAlchemyError as sae:
        # Catch and handle SQLAlchemy errors
        result = sqlalchemy_exception_handler(sae)
        return create_response(result)
    except Exception as exc:
        # Catch and handle Unhandled errors
        result = unhandled_exception_handler(exc)
        return create_response(result)
    else:
        return create_response(price_activation_status_update)

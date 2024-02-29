
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import get_query_param_value, create_response
from common_component.src.core.handlers.exception_handler import sqlalchemy_exception_handler, unhandled_exception_handler
from service import update_price_survey_activation
from gateway_survey_activation_schema import PriceActivation
from aws_lambda_powertools.utilities.parser import parse

log = Log().get_logger_service("Update Gateway Price Activation")


@log.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    log.info("Entered into event handler")
    log.set_correlation_id(context.aws_request_id)
    log.append_keys(log_stream=context.log_stream_name)
    try:
        """
        This is a router function update the gateway price survey activation status
        """
        log.append_keys(resource_path="/competitors/gatewayPriceActivation/updateGatewayPriceActivation")
        log.debug("Entered into update_survey_management_frequency Router")
        request = event['body']
        parsed_payload: PriceActivation = parse(request, model=PriceActivation)
        price_activation_status_update = update_price_survey_activation(parsed_payload)
        log.debug("Received response from update_price_survey_activation Service")
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

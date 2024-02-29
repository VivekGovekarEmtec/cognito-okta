from sqlalchemy.exc import SQLAlchemyError
from aws_lambda_powertools.utilities.typing import LambdaContext
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import get_query_param_value, create_response
from common_component.src.core.handlers.exception_handler import sqlalchemy_exception_handler, unhandled_exception_handler
from common_services.services.survey_schedule_service import get_survey_schedule_detail_by_site_id
from service import get_survey_schedule_detail
from enum import Enum
from common_component.src.core.helpers.helper import SortDirections

class SortName(str, Enum):
    siteId = "siteId"
    region = "region"
    kentId = "kentId"
    brandMarketer = "brandMarketer"
    address = "address"
    frequencyValues = "frequencyValues"
    productDescription = "productDescription"
    effectiveDate = "effectiveDate"
    expiryDate = "expiryDate"
    status = "status"
    kentid = ""
    time1 = "time1"
    time2 = "time2"
    time3 = "time3"
    time4 = "time4"
    time5 = "time5"

log = Log().get_logger_service("Get all unreviewed survey")


@log.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    log.info("Entered into event handler")
    log.set_correlation_id(context.aws_request_id)
    log.append_keys(log_stream=context.log_stream_name)
    log.append_keys(resource_path=event['path'])
    try:
        query_string_params = event["queryStringParameters"]
        site_id = get_query_param_value(query_string_params, "site_id",int)
        request_date = get_query_param_value(query_string_params, "request_date",str)
        competitor_status= get_query_param_value(query_string_params, "competitor_status",int)
        include_rows = get_query_param_value(query_string_params, "include_rows",int)
        language =get_query_param_value(query_string_params, "language",str)
        search_term = get_query_param_value(query_string_params, "search_term",str)
        sort_name = get_query_param_value(query_string_params, "sort_name",SortName)
        sort_direction = get_query_param_value(query_string_params, "sort_direction",SortDirections)
        page_number = get_query_param_value(query_string_params, "page_number",int)
        records = get_query_param_value(query_string_params, "records",int)
        lang =get_query_param_value(query_string_params, "lang",str)
        
        
        if(event['path'] == '/survey/getSurveyScheduleDetailBySiteId'):
            response_data = get_survey_schedule_detail_by_site_id(site_id,request_date,competitor_status,include_rows,language)
            log.debug("Received response from get_survey_schedule_detail_by_site_id Service")
        elif(event['path'] == '/survey/getSurveyScheduleDetail'):
           response_data = get_survey_schedule_detail(site_id, request_date, competitor_status,lang,search_term,sort_name, sort_direction,page_number,records)
           log.debug("Received response from get_survey_schedule_detail Service")
        else: 
            response_data = {
            "status_code": 404,
            "message": "Invalid api",
            "data": {}
        }

 
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

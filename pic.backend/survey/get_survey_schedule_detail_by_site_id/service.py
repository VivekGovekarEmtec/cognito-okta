from sqlalchemy import text
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
import json
from common_component.src.core.helpers.encoder import jsonable_encoder

#TODO - hardcoded constant value
db_instance = CreateDBConnection()
log = Log().get_logger_service("Survey schedule")


def get_survey_schedule_detail(site_id, request_date, competitor_status, lang, search_term, sort_name, sort_direction,
                               page_number, records):
    """
        This api is used to get all competitors
        """
    try:
        log.append_keys(service_function="get_survey_schedule_detail")
        log.debug("Entered into get_survey_schedule_detail service")
        with db_instance.create_writer_connection() as db:
            get_survey_schedule_detail_function_name = 'dbo.fn_survey_schedule_detail'
            query = text(
                "SELECT * from " + get_survey_schedule_detail_function_name + "(cast(:site_id AS character varying),cast(:request_date AS TIMESTAMP without time zone),cast(:lang AS character varying),:competitor_status,cast(:search_term AS character varying),cast(:sort_name AS character varying),cast(:sort_direction AS character varying),:page_number,:records)")
            parameters = {"site_id": site_id, "request_date": request_date, "lang": lang,
                          "competitor_status": competitor_status,
                          "search_term": search_term, "sort_name": sort_name,
                          "sort_direction": sort_direction, "page_number": page_number, "records": records}
            output = call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        total_search_count = output[0]["total_search_count"]
        total_count = output[0]["total_count"]
        response_data = jsonable_encoder(output)

        if total_count is None or total_count == 0:
           response = {
            "status_code": 204,
            "message": "Data not found in the database",
            "data": {"total_search_count": total_search_count, "total_count": total_count,
                     "survey_schedule_list": response_data}
        } 
        else:
            response = {
                "status_code": 200,
                "message": "Received all survey schedule data from Database successfully",
                "data": {"total_search_count": total_search_count, "total_count": total_count,
                        "survey_schedule_list": response_data}
            }
    except Exception as exc:
        raise exc
    else:
        log.debug("get_survey_schedule_detail service executed successfully")
        return response

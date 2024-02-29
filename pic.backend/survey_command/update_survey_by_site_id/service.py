from sqlalchemy import text
import json
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from survey_schema import UpdateCompetitorSites

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service()


def update_competitor_sites_by_site_id_service(competitor_site: UpdateCompetitorSites):
    """
    This function will update contacts in database
    """
    try:
        log.append_keys(service_function="update_competitor_sites_by_site_id_service")
        log.debug("Entered into update_competitor_sites_by_site_id_service service")
        with db_instance.create_writer_connection() as db:
            update_competitor_site_procedure_name = 'dbo.sp_competitor_site_prices_insert'
            val = json.loads(competitor_site.json())
            json_data = str(val['json_data']).replace("'", '"')
            query = text(
                "call " + update_competitor_site_procedure_name + "( :site_no,:survey_date,CAST(:reason_code AS character varying),CAST(:json_data AS character varying),CAST(:user_id AS character varying))")
            parameters = {"site_no": competitor_site.site_no,
                          "survey_date": competitor_site.survey_date,
                          "reason_code": competitor_site.reason_code,
                          "json_data": json_data,
                          "user_id": competitor_site.user_id}
            call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        response = {
            "status_code": 200,
            "message": "Deleted the survey management frequencies successfully",
            "data": {}
        }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        return response

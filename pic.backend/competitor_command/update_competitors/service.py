from sqlalchemy import text
import json
from update_manage_schema import UpdateCompetitor
from common_component.src.core.helpers.encoder import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log

db_instance = CreateDBConnection()
log = Log().get_logger_service()

def update_competitor(competitor: UpdateCompetitor):
    """
    This function calls database to update existing competitors
    """
    try:
        log.append_keys(service_function="update_competitor")
        log.debug("Entered into update_competitor service")
        with db_instance.create_writer_connection() as db:
            update_competitor_procedure_name = 'dbo.sp_competitor_update'
            query = text(
                "call " + update_competitor_procedure_name + "( :id, :kent_id, :brand_id,:marketer_id, CAST(:address AS character varying), CAST(:muni_name AS character varying), :province_id ,CAST(:restricted_dsl AS character varying) , CAST(:lat AS Numeric), CAST(:long AS Numeric), CAST(:last_user_id AS character varying), CAST(:lsd_sign AS smallint), :site_rating, CAST(:ml AS Numeric), CAST(:gas_buddy AS character varying), CAST(:wd_open AS character varying), CAST(:wd_close AS character varying), :status_code, CAST(:language AS character varying))")
            parameters = {"id": competitor.id, "kent_id": competitor.kent_id, "brand_id": competitor.brand_id,
                          "marketer_id": competitor.marketer_id, "address": competitor.address,
                          "muni_name": competitor.muni_name, "province_id": competitor.province_id,
                          "restricted_dsl": competitor.restricted_dsl, "lat": competitor.lat, "long": competitor.long,
                          "last_user_id": competitor.last_user_id, "lsd_sign": competitor.lsd_sign,
                          "site_rating": competitor.site_rating, "ml": competitor.ml, "gas_buddy": competitor.gas_buddy,
                          "wd_open": competitor.wd_open, "wd_close": competitor.wd_close,
                          "status_code": competitor.status_code, "language": competitor.language}
            call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")

        response = {
            "status_code": 200,
            "message": "Competitor Updated successfully",
            "data": {}
        }
    except SQLAlchemyError as sql_alchemy_exception:
        raise sql_alchemy_exception
    
    except Exception as exc:
        raise exc
    else:
        log.debug("update_competitor service executed successfully")
        return jsonable_encoder(response)
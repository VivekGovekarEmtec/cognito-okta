from sqlalchemy import text
import json
from association_schema import SaveCompetitorsAssociation
from common_component.src.core.helpers.encoder import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log

db_instance = CreateDBConnection()
log = Log().get_logger_service()

def save_competitors(save_competitors_association: SaveCompetitorsAssociation):
    """
    This function is used to save competitors
    """
    try:
        log.append_keys(service_function="save_competitors")
        log.debug("Entered into save_competitors service")
        with db_instance.create_writer_connection() as db:
            save_competitor_procedure_name = 'dbo.sp_competitor_site_xref_insert'
            val = json.loads(save_competitors_association.json())
            json_data = str(val['json_data']).replace("'", '"')
            query = text(
                "call " + save_competitor_procedure_name + "( :outlet_id, CAST(:json_data AS character varying),CAST(:push_to_pos AS numeric), CAST(:user_id AS character varying))")
            parameters = {"outlet_id": save_competitors_association.outlet_id, "json_data": json_data,
                          "push_to_pos": save_competitors_association.push_to_pos,
                          "user_id": save_competitors_association.user_id}
            call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        response = {
            "status_code": 200,
            "message": "Saved competitor association successfully",
            "data": {}
        }
    except SQLAlchemyError as sql_alchemy_exception:
        raise sql_alchemy_exception
    
    except Exception as exc:
        raise exc
    else:
        log.debug("save_competitors service executed successfully")
        return jsonable_encoder(response)
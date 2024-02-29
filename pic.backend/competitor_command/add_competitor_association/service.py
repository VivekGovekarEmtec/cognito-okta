from sqlalchemy import text
import json
from add_association_schema import AttachCompetitorsAssociationList
from common_component.src.core.helpers.encoder import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log

db_instance = CreateDBConnection()
log = Log().get_logger_service()

def attach_competitor_association(create_competitors_association: AttachCompetitorsAssociationList):
    """
    This function is used to add competitor from association screen
    """
    try:
        log.append_keys(service_function="attach_competitor_association")
        log.debug("Entered into attach_competitor_association service")
        with db_instance.create_writer_connection() as db:
            attach_competitor_procedure_name = 'dbo.sp_competitor_site_xref_for_adding_new_insert'
            val = json.loads(create_competitors_association.json())
            json_data = str(val['json_data']).replace("'", '"')
            query = text(
                "call " + attach_competitor_procedure_name + "( CAST(:json_data AS character varying), CAST(:user_id AS character varying))")
            parameters = {"json_data": json_data, "user_id": create_competitors_association.user_id}
            call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")

        response = {
            "status_code": 200,
            "message": "added competitor successfully",
            "data": {}
        }
    except SQLAlchemyError as sql_alchemy_exception:
        raise sql_alchemy_exception
    
    except Exception as exc:
        raise exc
    else:
        log.debug("attach_competitor_association service executed successfully")
        return jsonable_encoder(response)

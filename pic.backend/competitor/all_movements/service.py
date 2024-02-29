import json
from sqlalchemy import text
from typing import List
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.encoder import jsonable_encoder

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service()

def get_site_tactical_movements(site_id: int, language: str, is_editable: bool):
    """
    This function is used to return all site tactical movements
    """
    try:
        log.append_keys(service_function="get_site_tactical_movements")
        log.debug("Entered into get_site_tactical_movements service")
        with db_instance.create_writer_connection() as db:
            is_editable = is_editable
            get_site_tactical_function_name = 'dbo.fn_site_tactics_select_all'
            query = text("SELECT * from " + get_site_tactical_function_name + "(:site_id,:language)")
            parameters = {"site_id": site_id, "language": language}
            output = call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        response_data = jsonable_encoder(output)
        # Convert follow_options and remove follow_option_names
        for item in response_data:
            item["follow_options"] = convert_follow_options_to_list(item.get("follow_options", ""),
                                                                    item.get("follow_option_names", ""))
            item.pop("follow_option_names", None)
        if len(response_data) == 0:
            response = {
            "status_code": 204,
            "message": "Data not found in the database",
            "data": None
        }
        else:
            response = {
            "status_code": 200,
            "message": "Received site tactical movements data from Database successfully",
            "data": {"site_tactical_movements_list": response_data}
        }

    except Exception as exc:
        raise exc
    else:
        log.debug("get_site_tactical_movements service executed successfully")
        return response

def convert_follow_options_to_list(follow_options_str: str, follow_option_names_str: str) -> List[dict]:
    """
    Convert comma-separated strings into lists of objects
    """
    if follow_options_str and follow_option_names_str:
        follow_option_ids = [option_id.strip() for option_id in follow_options_str.split(',')]
        follow_option_names = [name.strip() for name in follow_option_names_str.split(',')]
        return [{"follow_option_id": option_id, "follow_option_name": name} for option_id, name in
                zip(follow_option_ids, follow_option_names)]
    else:
        log.debug("convert_follow_options_to_list service executed successfully")
        return []
from sqlalchemy import text
import json
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log

db_instance = CreateDBConnection()
log = Log().get_logger_service()

def get_multi_competitors(site_id: int, lang: str):
    try:
        log.append_keys(service_function="get_multi_competitors")
        log.debug("Entered into get_multi_competitors service")
        with db_instance.create_writer_connection() as db:
            get_function_name = 'dbo.fn_site_competitors_org_select'
            query = text("SELECT * from " + get_function_name + "(:site_id, CAST(:lang AS character varying))")
            parameters = {"site_id": site_id, 'lang': lang}
            output = call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        output = transform_hierarchy(output)
        response = {
            "status_code": 200,
            "message": "get the competitors hierarchy data successfully",
            "data": {"competitor_hierarchy_data": output}
        }
    except SQLAlchemyError as sql_alchemy_exception:
        raise sql_alchemy_exception
    
    except Exception as exc:
        raise exc
    else:
        log.debug("get_multi_competitors service executed successfully")
        return response

def transform_hierarchy(input_array):
    result = []
    node_dict = {node["_id"]: node for node in input_array}

    def process_node(node_id):
        node = node_dict[node_id]
        return {
            "id": node["_id"],
            "title": node["_node_desc"],
            "regular_price": node["_die_price"],
            "diesel_price": node["_reg_price"],
            "display_order": node["_display_order"],
            "unselectable": str(node["_id"]) == '-1' or str(node["_id"]) == '0',
            "children": []
        }

    def build_hierarchy(parent_id):
        children = []
        for node_id, node in node_dict.items():
            if node["_parent_id"] == parent_id and node_id != -1:
                child = {
                    "id": node["_id"],
                    "title": node["_node_desc"],
                    "regular_price": node["_die_price"],
                    "diesel_price": node["_reg_price"],
                    "display_order": node["_display_order"],
                    "unselectable": str(node["_id"]) == '-1' or str(node["_id"]) == '0',
                    "children": build_hierarchy(node_id)
                }
                if child["children"]:
                    children.append(child)
                else:
                    children.append(process_node(node_id))
        return children

    root_nodes = [node for node in input_array if node["_id"] == -1]

    for root_node in root_nodes:
        result.append({
            "id": root_node["_id"],
            "title": root_node["_node_desc"],
            "regular_price": root_node["_die_price"],
            "diesel_price": root_node["_reg_price"],
            "display_order": root_node["_display_order"],
            "unselectable": str(root_node["_id"]) == '-1' or str(root_node["_id"]) == '0',
            "children": build_hierarchy(root_node["_id"])
        })
    log.debug("transform_hierarchy service executed successfully")
    return result
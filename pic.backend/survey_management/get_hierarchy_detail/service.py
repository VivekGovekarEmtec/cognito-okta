from sqlalchemy import text
import json
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service()


def get_hierarchy_detail(hierarchy_id: int, product_id: str):
    """
        This function used to get hierarchy for survey management
    """
    try:
        log.append_keys(service_function="get_hierarchy_detail")
        log.debug("Entered into get_hierarchy_detail service")
        with db_instance.create_writer_connection() as db:
            hierarchy_survey_management_function_name = "dbo.fn_hierarchy_detail"
            param_dict = {
                "hierarchy_id": hierarchy_id,
                "product_id": product_id
            }
            query = text('select * from ' + hierarchy_survey_management_function_name +
                         '(:hierarchy_id,:product_id)')
            response_data = call_postgres_function(query=query, db=db, parameters=param_dict)
        output_data = transform_hierarchy(response_data)
        response = {
            "status_code": 200,
            "message": "get the survey management hierarchy successfully",
            "data": {"hierarchy_detail_data": output_data}
        }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        return response

def transform_hierarchy(input_array):
    station_list = {}
    for item in input_array:
        if item['_parent_id'] in station_list: 
            if item['stations'] != None and item['stations'] not in station_list[item['_parent_id']]:
                station_list[item['_parent_id']] = ','.join([station_list[item['_parent_id']],item['stations']])
        else:
            station_list[item['_parent_id']] =item['stations']
    result = []
    node_dict = {node["_id"]: node for node in input_array}

    def process_node(node_id):
        node = node_dict[node_id]
        return {
            "id": node["_id"],
            "title": node["_node_desc"],
            "diesel_price": node["_die_price"],
            "regular_price": node["_reg_price"],
            "temp_close_status": node["_temp_close_status"],
            "site_id": node["_site_id"],
            "prod_hold": node["_prod_hold"],
            "station_no": node["stations"],
            "children": []
        }

    def build_hierarchy(parent_id):
        children = []
        for node_id, node in node_dict.items():
            print(node_id)
            if node["_parent_id"] == parent_id:
                child = {
                    "id": node_id,
                    "title": node["_node_desc"],
                    "diesel_price": node["_die_price"],
                    "regular_price": node["_reg_price"],
                    "temp_close_status": node["_temp_close_status"],
                    "site_id": node["_site_id"],
                    "prod_hold": node["_prod_hold"],
                    "station_no": station_list[node_id] if node_id in station_list else '',
                    "children": build_hierarchy(node_id)
                }
                if child["children"]:
                    children.append(child)
                else:
                    children.append(process_node(node_id))
        return children

    root_nodes = [node for node in input_array if node["_parent_id"] == -1]

    for root_node in root_nodes:
        result.append({
            "id": root_node["_id"],
            "title": root_node["_node_desc"],
            "diesel_price": root_node["_die_price"],
            "regular_price": root_node["_reg_price"],
            "temp_close_status": root_node["_temp_close_status"],
            "site_id": root_node["_site_id"],
            "prod_hold": root_node["_prod_hold"],
            "station_no": root_node["stations"],
            "children": build_hierarchy(root_node["_id"])
        })
    return result

from sqlalchemy import text
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.encoder import jsonable_encoder

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service("Station master Get OutletDetailsByOutletNo")


def get_outlet_configuration_by_site_id(site_id: int):
    """
    This function is used to return all outlets
    """
    try:
        log.append_keys(service_function="get_outlet_configuration_by_site_id")
        log.debug("Entered into get_outlet_configuration_by_site_id service")
        with db_instance.create_writer_connection() as db:
            get_outlet_by_id_function_name = 'dbo.fn_site_configuration_by_siteid'
            query = text("SELECT * from " + get_outlet_by_id_function_name + "(:site_id)")
            parameters = {"site_id": site_id}
            output = call_postgres_function(query, parameters, db)
        log.debug("Received response from database")
        response_data = jsonable_encoder(output[0])

    except Exception as exc:
        raise exc
    else:
        log.debug("get_outlet_configuration_by_site_id service executed successfully")
        return response_data

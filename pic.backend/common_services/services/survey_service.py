from sqlalchemy import text
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log

# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()
log = Log().get_logger_service("Survey service")


def frequency_value_calculation(frequency: str, language: str):
    try:
        log.append_keys(service_function="frequency_value_calculation")
        log.debug("Entered into frequency_value_calculation service")
        with db_instance.create_writer_connection() as db:
            get_frequency_function_name = "dbo.fn_frequency"
            param_dict = {"language": language}
            query = text(
                'SELECT frequency_code FROM '
                + get_frequency_function_name + '(:language)')
            days_code = call_postgres_function(query=query, db=db, parameters=param_dict)
        log.debug("Received response from database")
        day = [d['frequency_code'] for d in days_code]
        freq_list = list(frequency)
        data = tuple(zip(freq_list, day))
        result = ""
        for val in data:
            if val[0] == "1":
                result = result + val[1] + "/"
        return result.rstrip("/")
    except Exception as e:
        print(e)
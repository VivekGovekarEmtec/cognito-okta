import json
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from schema import UpdateRegulatedPrice
from common_component.src.core.helpers.encoder import jsonable_encoder

log = Log().get_logger_service("Create price on hold")
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()


def update_regulated_price(regulated_price: UpdateRegulatedPrice):
    """
    This function will update regulated price in database
    """
    try:
        log.append_keys(service_function="update_regulated_price")
        log.debug("Entered into update_regulated_price service")
        with db_instance.create_writer_connection() as db:
            update_regulated_price_procedure_name = 'dbo.sp_regulated_prices_details_update'
            val = json.loads(regulated_price.json())
            json_data = str(val['json_data']).replace("'", '"')
            query = text(
                "call " + update_regulated_price_procedure_name + "( :authorization_number,CAST(:user_id AS character varying),CAST(:json_data AS jsonb))")
            parameters = {"authorization_number": regulated_price.authorization_number,
                          "json_data": json_data,
                          "user_id": regulated_price.user_id}
            call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        response = {
            "status_code": 200,
            "message": "Updated the new brunswick regulated price in Database successfully",
            "data": {}
        }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as e:
        raise e
    else:
        log.debug("update_regulated_price service executed successfully")
        return jsonable_encoder(response)

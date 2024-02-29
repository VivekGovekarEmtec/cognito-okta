from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from schema import InsertPriceHeader
from common_component.src.core.helpers.encoder import jsonable_encoder

log = Log().get_logger_service("Create price on hold")
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()


def submit_regulated_price_header(price: InsertPriceHeader):
    """
    This API is used to create regulated prices header in the database.
    """
    try:
        log.append_keys(service_function="submit_regulated_price_header")
        log.debug("Entered into submit_regulated_price_header service")
        with db_instance.create_writer_connection() as db:
            _regulated_price_type_id = 2
            submit_regulated_price_header_procedure_name = 'dbo.sp_regulated_prices_header_ns_insert'
            query = text(
                "call " + submit_regulated_price_header_procedure_name + "(:_authorization_number,"
                                                                         ":_regulated_price_type_id,"
                                                                         "CAST(:_effective_date AS timestamp without "
                                                                         "time zone),"
                                                                         "CAST(:_file_input AS character varying), "
                                                                         ":_zone1_regular_min,"
                                                                         ":_zone1_regular_max,:_zone1_diesel_min, "
                                                                         ":_zone1_diesel_max, :_zone2_regular_min, "
                                                                         ":_zone2_regular_max, :_zone2_diesel_min, "
                                                                         ":_zone2_diesel_max,:_zone3_regular_min, "
                                                                         ":_zone3_regular_max, :_zone3_diesel_min,"
                                                                         ":_zone3_diesel_max, :_zone4_regular_min, "
                                                                         ":_zone4_regular_max,:_zone4_diesel_min, "
                                                                         ":_zone4_diesel_max, :_zone5_regular_min,"
                                                                         ":_zone5_regular_max, :_zone5_diesel_min, "
                                                                         ":_zone5_diesel_max,:_zone6_regular_min, "
                                                                         ":_zone6_regular_max, :_zone6_diesel_min, "
                                                                         ":_zone6_diesel_max, :_zone1_plus_min, "
                                                                         ":_zone1_plus_max,:_zone1_supreme_min, "
                                                                         ":_zone1_supreme_max, :_zone2_plus_min,"
                                                                         ":_zone2_plus_max, :_zone2_supreme_min, "
                                                                         ":_zone2_supreme_max,:_zone3_plus_min, "
                                                                         ":_zone3_plus_max, :_zone3_supreme_min,"
                                                                         ":_zone3_supreme_max, :_zone4_plus_min, "
                                                                         ":_zone4_plus_max,:_zone4_supreme_min, "
                                                                         ":_zone4_supreme_max, :_zone5_plus_min, "
                                                                         ":_zone5_plus_max, :_zone5_supreme_min, "
                                                                         ":_zone5_supreme_max,:_zone6_plus_min, "
                                                                         ":_zone6_plus_max, :_zone6_supreme_min,"
                                                                         ":_zone6_supreme_max, CAST(:_inserted_user_id AS character varying))"
            )
            parameters = {
                "_authorization_number": price.authorization_number,
                "_regulated_price_type_id": _regulated_price_type_id,
                "_effective_date": price.effective_date,
                "_file_input": price.file_input,
                "_zone1_regular_min": price.zone1_regular_min,
                "_zone1_regular_max": price.zone1_regular_max,
                "_zone1_diesel_min": price.zone1_diesel_min,
                "_zone1_diesel_max": price.zone1_diesel_max,
                "_zone2_regular_min": price.zone2_regular_min,
                "_zone2_regular_max": price.zone2_regular_max,
                "_zone2_diesel_min": price.zone2_diesel_min,
                "_zone2_diesel_max": price.zone2_diesel_max,
                "_zone3_regular_min": price.zone3_regular_min,
                "_zone3_regular_max": price.zone3_regular_max,
                "_zone3_diesel_min": price.zone3_diesel_min,
                "_zone3_diesel_max": price.zone3_diesel_max,
                "_zone4_regular_min": price.zone4_regular_min,
                "_zone4_regular_max": price.zone4_regular_max,
                "_zone4_diesel_min": price.zone4_diesel_min,
                "_zone4_diesel_max": price.zone4_diesel_max,
                "_zone5_regular_min": price.zone5_regular_min,
                "_zone5_regular_max": price.zone5_regular_max,
                "_zone5_diesel_min": price.zone5_diesel_min,
                "_zone5_diesel_max": price.zone5_diesel_max,
                "_zone6_regular_min": price.zone6_regular_min,
                "_zone6_regular_max": price.zone6_regular_max,
                "_zone6_diesel_min": price.zone6_diesel_min,
                "_zone6_diesel_max": price.zone6_diesel_max,
                "_zone1_plus_min": price.zone1_plus_min,
                "_zone1_plus_max": price.zone1_plus_max,
                "_zone1_supreme_min": price.zone1_supreme_min,
                "_zone1_supreme_max": price.zone1_supreme_max,
                "_zone2_plus_min": price.zone2_plus_min,
                "_zone2_plus_max": price.zone2_plus_max,
                "_zone2_supreme_min": price.zone2_supreme_min,
                "_zone2_supreme_max": price.zone2_supreme_max,
                "_zone3_plus_min": price.zone3_plus_min,
                "_zone3_plus_max": price.zone3_plus_max,
                "_zone3_supreme_min": price.zone3_supreme_min,
                "_zone3_supreme_max": price.zone3_supreme_max,
                "_zone4_plus_min": price.zone4_plus_min,
                "_zone4_plus_max": price.zone4_plus_max,
                "_zone4_supreme_min": price.zone4_supreme_min,
                "_zone4_supreme_max": price.zone4_supreme_max,
                "_zone5_plus_min": price.zone5_plus_min,
                "_zone5_plus_max": price.zone5_plus_max,
                "_zone5_supreme_min": price.zone5_supreme_min,
                "_zone5_supreme_max": price.zone5_supreme_max,
                "_zone6_plus_min": price.zone6_plus_min,
                "_zone6_plus_max": price.zone6_plus_max,
                "_zone6_supreme_min": price.zone6_supreme_min,
                "_zone6_supreme_max": price.zone6_supreme_max,
                "_inserted_user_id": price.inserted_user_id,
            }
            output = call_postgres_function(query=query, parameters=parameters, db=db)
            result_data = output.mappings().all()
        log.debug("Received response from database")
        response = {
            "status_code": 200,
            "message": "Regulated prices header added successfully",
            "data": result_data[0]
        }

    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        log.debug("submit_regulated_price_header service executed successfully")
        return jsonable_encoder(response)

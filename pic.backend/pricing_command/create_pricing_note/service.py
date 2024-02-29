from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from schema import CreatePricingNote
from common_component.src.core.helpers.encoder import jsonable_encoder

log = Log().get_logger_service("Create price on hold")
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()


def save_note(pricing_config: CreatePricingNote):
    try:
        log.append_keys(service_function="save_note")
        log.debug("Entered into save_note service")

        with db_instance.create_writer_connection() as db:
            save_note_procedure_name = "dbo.sp_site_note_update"
            param_dict = {
                "site_id": pricing_config.site_id,
                "gaz_note": pricing_config.gaz_note,
                "gaz_note_last_user": pricing_config.gaz_note_last_user,
                "gaz_note_last_change_date": pricing_config.gaz_note_last_change_date,
                "dsl_note": pricing_config.dsl_note,
                "dsl_note_last_user": pricing_config.dsl_note_last_user,
                "dsl_note_last_change_date": pricing_config.dsl_note_last_change_date,
                "promo_note": pricing_config.promo_note,
                "promo_note_last_user": pricing_config.promo_note_last_user,
                "promo_note_last_change_date": pricing_config.promo_note_last_change_date,
                "temporary_note": pricing_config.temporary_note,
                "temporary_note_last_user": pricing_config.temporary_note_last_user,
                "temporary_note_last_change_date": pricing_config.temporary_note_last_change_date,
                "user_id": pricing_config.user_id
            }
            query = text(
                'CALL '
                + save_note_procedure_name +
                '(:site_id,'
                'CAST(:gaz_note as Text),'
                'CAST(:gaz_note_last_user as character varying),'
                ':gaz_note_last_change_date,'
                'CAST(:dsl_note as TEXT),'
                'CAST(:dsl_note_last_user as character varying),'
                ':gaz_note_last_change_date,'
                'CAST(:promo_note as TEXT),'
                'CAST(:promo_note_last_user as character varying),'
                ':promo_note_last_change_date,'
                'CAST(:temporary_note as TEXT),'
                'CAST(:temporary_note_last_user as character varying),'
                ':temporary_note_last_change_date,'
                'CAST(:user_id as character varying))')

            call_postgres_function(query=query, parameters=param_dict, db=db)
        log.debug("Received response from database")
        response = {
            "status_code": 200,
            "message": "Note saved successfully",
            "data": {}
        }

    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as e:
        raise e
    else:
        log.debug("save_note service executed successfully")
        return jsonable_encoder(response)


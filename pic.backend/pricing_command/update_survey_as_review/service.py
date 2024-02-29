from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from schema import MarkReview
from common_component.src.core.helpers.encoder import jsonable_encoder

log = Log().get_logger_service("Create price on hold")
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()


def mark_survey_review_update_service(review: MarkReview):
    """
    This function will Update the survey as reviewed in database
    """
    try:
        log.append_keys(service_function="mark_survey_review_update_service")
        log.debug("Entered into mark_survey_review_update_service service")

        with db_instance.create_writer_connection() as db:
            update_pending_review_name = 'dbo.sp_competitor_site_prices_mark_as_review_update'
            query = text(
                "call " + update_pending_review_name + "( :site_id,CAST(:user_id AS character varying))")
            parameters = {"site_id": review.site_id, "user_id": review.user_id}
            call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        response = {
            "status_code": 200,
            "message": "Updated the survey as reviewed in Database successfully",
            "data": {}
        }
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as e:
        raise e
    else:
        log.debug("mark_survey_review_update_service service executed successfully")
        return jsonable_encoder(response)

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from schema import MarkReview
from common_component.src.core.helpers.encoder import jsonable_encoder

log = Log().get_logger_service("Create price on hold")
# Create an instance of the CreateDBConnection class
db_instance = CreateDBConnection()


def update_pending_review_service(pending_review: MarkReview):
    """
    This function will update contacts in database
    """
    try:
        log.append_keys(service_function="update_pending_review_service")
        log.debug("Entered into update_pending_review_service service")
        with db_instance.create_writer_connection() as db:
            update_pending_review_name = 'dbo.sp_competitor_site_prices_mark_as_pending_review_update'
            query = text(
                "call " + update_pending_review_name + "( :site_id,CAST(:user_id AS character varying))")
            parameters = {"site_id": pending_review.site_id,
                          "user_id": pending_review.user_id}
            call_postgres_function(query=query, parameters=parameters, db=db)
        log.debug("Received response from database")
        response = {
            "status_code": 200,
            "message": "Updated the pending review in Database successfully",
            "data": {}
        }

    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        log.debug("update_pending_review_service service executed successfully")
        return jsonable_encoder(response)

from sqlalchemy import text
import json
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.repositories.data_repository import call_postgres_function, CreateDBConnection
from common_component.src.core.utils.Logger import Log
from common_component.src.core.helpers.helper import remove_keys
from common_component.src.core.helpers.encoder import jsonable_encoder


db_instance = CreateDBConnection()
log = Log().get_logger_service()


def get_unreviewed_survey(language: str, search_term: str, sort_name: str, sort_direction: str, page_number: int,
                          records: int):
    """
    This function is used to get all unreviewed surveys
    """
    try:
        with db_instance.create_writer_connection() as db:
            get_unreviewed_survey_function_name = "dbo.fn_survey_to_review"
            param_dict = {
                "language": language,
                "search_term": search_term,
                "sort_name": sort_name,
                "sort_direction": sort_direction,
                "page_number": page_number,
                "records": records
            }
            query = text(
                'SELECT * FROM '
                + get_unreviewed_survey_function_name +
                '(:language,:search_term,:sort_name,:sort_direction,:page_number,:records)')

        output = call_postgres_function(query=query, db=db, parameters=param_dict)
        total_search_count = output[0]['total_search_count']
        total_count = output[0]['total_count']

        response_data = jsonable_encoder(output)
        
        if total_count is None or total_count == 0:
            response = {
            "status_code":204,
            "message": "Total count is 0",
            "data": None
        }
        else:
            response = {
                "status_code": 200,
                "message": "Received the unreviewed survey from database successfully",
                "data": {"total_search_count": total_search_count, "total_count": total_count,
                        "unreviewed_surveys_list": response_data}
            }

        
    except SQLAlchemyError as sql_alchemy_exception:
        # Catch and handle SQLAlchemy errors
        raise sql_alchemy_exception
    except Exception as exc:
        raise exc
    else:
        return response

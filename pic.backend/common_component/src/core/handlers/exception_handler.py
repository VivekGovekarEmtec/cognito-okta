import json
from sqlalchemy.exc import SQLAlchemyError
from common_component.src.core.resources.constants import SQL_ALCHEMY_UNDEFINED_FUNCTION, SQL_ALCHEMY_DATA_NOT_FOUND, \
    SQL_ALCHEMY_UNIQUE_VIOLATION, SQL_ALCHEMY_INVALID_PARAMETER_VALUE, SQL_ALCHEMY_NUMERIC_VALUE_OUT_OF_RANGE, \
    SQL_ALCHEMY_RAISE_EXCEPTION, SQL_ALCHEMY_FOREIGN_KEY_VIOLATION, SQL_ALCHEMY_UNDEFINED_COLUMN
from common_component.src.core.utils.Logger import Log

###
# Exception Handlers for filter exception error and personalize messages
###
log = Log().get_logger_service('Exception handler logs')


def sqlalchemy_exception_handler(exc: SQLAlchemyError) -> json:
    """
    This is a wrapper to the default sql alchemy handler of FastAPI.
    This function will be called when a sql alchemy is explicitly raised.
    """
    status_code = 204
    log.debug("sql alchemy error was invoked")
    log.error(exc)
    response = None
    if hasattr(exc, 'orig') and hasattr(exc.orig, 'pgcode'):
        postgres_error_code = exc.orig.pgcode
        if postgres_error_code in [SQL_ALCHEMY_UNDEFINED_FUNCTION, SQL_ALCHEMY_UNDEFINED_COLUMN]:
            status_code = 404
            response = {
                "status_code": status_code,
                "message": 'Undefined function or column',
                "error": str(exc)
            }
            log.error(response)
        elif postgres_error_code in [SQL_ALCHEMY_DATA_NOT_FOUND, SQL_ALCHEMY_RAISE_EXCEPTION]:
            status_code = 204
            response = {
                "status_code": status_code,
                "message": 'Data not found',
                "error": str(exc)
            }
            log.error(response)
        elif postgres_error_code in [SQL_ALCHEMY_INVALID_PARAMETER_VALUE, SQL_ALCHEMY_UNIQUE_VIOLATION,
                                     SQL_ALCHEMY_NUMERIC_VALUE_OUT_OF_RANGE]:
            status_code = 422
            response = {
                "status_code": status_code,
                "message": 'Invalid parameter value',
                "error": str(exc)
            }
            log.error(response)
        elif postgres_error_code in [SQL_ALCHEMY_FOREIGN_KEY_VIOLATION]:
            status_code = 500
            response = {
                "status_code": status_code,
                "message": 'Foreign Key Violation Error',
                "error": str(exc)
            }
            log.error(response)
        else:
            status_code = 500
            response = {
                "status_code": status_code,
                "message": 'Internal server error',
                "error": str(exc)
            }
            log.error(response)
    else:
        # return None
        status_code = 500
        response = {
            "status_code": status_code,
            "message": 'Internal server error',
            "error": str(exc)
        }
        log.error(response)
    return response


def value_exception_handler(exc: ValueError) -> json:
    """
    This middleware will log all value exceptions.
    """
    log.debug("Value Exception is raised")
    error_message = f"Bad Request"
    status_code = 400
    response = {
        "status_code": status_code,
        "message": error_message,
        "error": str(exc)
    }
    return response


def unhandled_exception_handler(exc: Exception) -> json:
    """
    This middleware will log all unhandled exceptions.
    Unhandled exceptions are all exceptions that are not HTTPExceptions or RequestValidationErrors.
    """
    print("this is exception -> ", str(exc))
    log.debug("Custom unhandled_exception_handler was called")
    error_message = f"Internal Server Error: {str(exc)}"
    status_code = 500
    response = {
        "status_code": status_code,
        "message": error_message,
        "error": str(exc)
    }
    return response

from aws_lambda_powertools.logging.logger import Logger

# We can remove this after refactor
logger: Logger = Logger()
logger.setLevel("DEBUG")


class Log:
    log: Logger

    def get_logger_service(self, service_name=None):
        if service_name is not None:
            Log.log = Logger(service=service_name)
        else:
            Log.log = Logger()
        Log.log.setLevel("DEBUG")
        return Log.log

import logging
import os
import sys
from pprint import pformat

from loguru import logger
from loguru._defaults import LOGURU_FORMAT


class InterceptHandler(logging.Handler):
    """Intercept standard logging messages toward Loguru sinks.

    Default handler from examples in loguru documentation. See
    https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    """

    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def format_record(record: dict) -> str:
    """Custom format for loguru loggers. Uses pformat for log any data like
    request/response body during debug. Works with logging if loguru handler
    it.

    Example:
    >> payload = [
           {
               "users": [
                   {"name": "Nick", "age": 87, "is_active": True},
                   {"name": "Alex", "age": 27, "is_active": True},
               ],
               "count": 2,
           }
       ]

    >> logger.bind(payload=payload).debug("users payload")
    >> [   {   'count': 2,
               'users': [   {'age': 87, 'is_active': True, 'name': 'Nick'},
                            {'age': 27, 'is_active': True, 'name': 'Alex'}]}]
    """
    format_string = LOGURU_FORMAT

    if record["extra"].get("payload") is not None:
        record["extra"]["payload"] = pformat(
            record["extra"]["payload"], indent=4, compact=True, width=88
        )
        format_string += "\n<level>{extra[payload]}</level>"

    format_string += "{exception}\n"
    return format_string


#############
# Root logger
#############

# All logs are handled via loguru
logging.getLogger().handlers = [InterceptHandler()]

# Set loguru logs format
logger.configure(
    handlers=[
        {
            "sink": sys.stdout,
            "level": logging.getLevelName(os.environ.get("LOG_LEVEL", "INFO")),
            "format": format_record,
            "serialize": os.environ.get("LOG_JSON_FORMAT", "false") == "true",
        },
    ],
    extra={"agent": None},
)

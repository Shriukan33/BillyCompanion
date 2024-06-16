import logging
import os
from typing import Any

from django.core.handlers.wsgi import WSGIHandler
from gunicorn.app.base import BaseApplication
from gunicorn.glogging import Logger

from billy_project.wsgi import application
from core.loggers import InterceptHandler

LOG_LEVEL = logging.getLevelName(os.environ.get("LOG_LEVEL", "INFO"))
GUNICORN_WORKERS = int(os.environ.get("GUNICORN_WORKERS", "2"))
GUNICORN_TIMEOUT = int(os.environ.get("GUNICORN_TIMEOUT", "30"))


class StubbedGunicornLogger(Logger):
    """Override Gunicorn's own logging configuration so its logs can be
    formatted like the rest.

    https://github.com/benoitc/gunicorn/issues/1572#issuecomment-430747811
    """

    def setup(self, _cfg: Any) -> None:
        handler = logging.NullHandler()
        self.error_logger = logging.getLogger("gunicorn.error")
        self.error_logger.addHandler(handler)
        self.access_logger = logging.getLogger("gunicorn.access")
        self.access_logger.addHandler(handler)
        self.error_log.setLevel(LOG_LEVEL)
        self.access_log.setLevel(LOG_LEVEL)


class GunicornApplication(BaseApplication):
    """Our Gunicorn application.

    Straight from the gunicorn documentation.
    https://docs.gunicorn.org/en/stable/custom.html
    """

    def __init__(self, app: WSGIHandler, options: dict | None = None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self) -> None:
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self) -> WSGIHandler:
        return self.application


if __name__ == "__main__":
    seen: set = set()
    for name in [
        *logging.root.manager.loggerDict,
        "gunicorn",
        "gunicorn.access",
        "gunicorn.error",
    ]:
        if name not in seen:
            seen.add(name.split(".")[0])
            logging.getLogger(name).handlers = [InterceptHandler()]

    options = {
        "bind": "0.0.0.0:8000",
        "workers": GUNICORN_WORKERS,
        "accesslog": "-",
        "timeout": GUNICORN_TIMEOUT,
        # Here we only keep subset of info since the logs are handled by loguru
        # and info like level/timestamp are automatically added.
        # See possible options at https://docs.gunicorn.org/en/0.17.0/configure.html#access-log-format
        "access_log_format": '"%(r)s" %(s)s "%(a)s"',
        "errorlog": "-",
        "logger_class": StubbedGunicornLogger,
    }

    GunicornApplication(application, options).run()

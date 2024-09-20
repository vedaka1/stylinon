import logging.handlers
from typing import Any

logger_config_dict: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "%(asctime)s - %(levelname)s - %(message)s"},
        "detailed": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "detailed",
            "level": "INFO",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "detailed",
            "filename": "my_app.log",
            "maxBytes": 10000,
            "backupCount": 3,
        },
    },
    # "loggers": {
    #     "uvicorn": {"handlers": ["console"], "level": "INFO", "propagate": False},
    #     "fastapi": {"handlers": ["console"], "level": "INFO", "propagate": False},
    #     "app": {"handlers": ["console", "file"], "level": "DEBUG", "propagate": True},
    # },
    "loggers": {"root": {"level": "DEBUG", "handlers": ["console", "file"]}},
}

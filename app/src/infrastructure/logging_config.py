import logging
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
            "level": logging.INFO,
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "app.log",
            "formatter": "simple",
            "level": logging.ERROR,
        },
    },
    # "loggers": {
    #     "uvicorn": {"handlers": ["console"], "level": "INFO", "propagate": False},
    #     "fastapi": {"handlers": ["console"], "level": "INFO", "propagate": False},
    #     "app": {"handlers": ["console", "file"], "level": "DEBUG", "propagate": True},
    # },
    "loggers": {"root": {"level": "DEBUG", "handlers": ["console"]}},
}

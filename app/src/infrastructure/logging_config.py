from typing import Any

logger_config_dict_dev: dict[str, Any] = {
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
            "level": "ERROR",
            "formatter": "detailed",
            "filename": "my_app.log",
            "maxBytes": 10000,
            "backupCount": 3,
        },
    },
    "loggers": {
        "root": {
            "level": "DEBUG",
            "handlers": ["console"],
        },
    },
}

logger_config_dict_prod: dict[str, Any] = {
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
            "level": "ERROR",
            "formatter": "detailed",
            "filename": "my_app.log",
            "maxBytes": 100000,
            "backupCount": 3,
        },
        "queue_handler": {
            "class": "logging.handlers.QueueHandler",
            "handlers": ["console", "file"],
            "respect_handler_level": True,
        },
    },
    "loggers": {
        "root": {
            "level": "INFO",
            "handlers": ["console", "file"],
        },
    },
}

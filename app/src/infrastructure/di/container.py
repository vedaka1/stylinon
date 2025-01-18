import logging
import logging.config
from functools import lru_cache
from multiprocessing import Queue

import logging_loki
from dishka import AsyncContainer, make_async_container
from src.infrastructure.logging_config import logger_config_dict_prod

from .database import DatabaseAdaptersProvider, DatabaseConfigurationProvider
from .gateways import GatewayProvider
from .security import SecurityProvider
from .settings import SettingsProvider
from .usecases import UseCasesProvider


@lru_cache(1)
def init_logger() -> None:
    logging.config.dictConfig(logger_config_dict_prod)
    return None


@lru_cache(1)
def init_loki_logger(app_name: str = 'app') -> logging_loki.LokiQueueHandler:
    return logging_loki.LokiQueueHandler(
        Queue(-1),
        url='http://loki:3100/loki/api/v1/push',
        tags={'application': app_name},
        version='1',
    )


@lru_cache(1)
def get_container() -> AsyncContainer:
    return make_async_container(
        SettingsProvider(),
        SecurityProvider(),
        DatabaseConfigurationProvider(),
        DatabaseAdaptersProvider(),
        UseCasesProvider(),
        GatewayProvider(),
    )

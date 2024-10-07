import logging
import logging.config
from functools import lru_cache

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
def get_container() -> AsyncContainer:
    return make_async_container(
        SettingsProvider(),
        SecurityProvider(),
        DatabaseConfigurationProvider(),
        DatabaseAdaptersProvider(),
        UseCasesProvider(),
        GatewayProvider(),
    )

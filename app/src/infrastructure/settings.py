import os
from dataclasses import dataclass
from typing import Any


def get_env_var(key: str, to_cast: Any, default: Any | None = None) -> Any:
    """
    Converting environment variable types
    ### Args:
        key (str): environment variable
        to_cast (Any): type to convert
        default (Any, optional): default value
    ### Raises:
        RuntimeError: occurs if such a variable is not found in .env and default is not set
    ### Returns:
        Any: an environment variable with a converted type
    """
    value = os.getenv(key)

    if not value and not default:
        raise RuntimeError(f"{key} environment variable not set")
    if not value:
        return default
    return to_cast(value)


@dataclass(frozen=True)
class TochkaBankSettings:

    TOKEN: str
    PUBLIC_KEY: str
    ALGORITHM: str

    @staticmethod
    def load_from_env() -> "TochkaBankSettings":
        return TochkaBankSettings(
            TOKEN=get_env_var("TOCHKA_TOKEN", to_cast=str, default="working_token"),
            PUBLIC_KEY=get_env_var("ACQUIRING_PUBLIC_KEY", to_cast=str),
            ALGORITHM=get_env_var("ACQUIRING_ALGORITHM", to_cast=str, default="RS256"),
        )


@dataclass(frozen=True)
class DatabaseSettings:

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @property
    def DB_URL(self) -> str:
        return "postgresql+asyncpg://{0}:{1}@{2}:{3}/{4}".format(
            self.POSTGRES_USER,
            self.POSTGRES_PASSWORD,
            self.POSTGRES_HOST,
            self.POSTGRES_PORT,
            self.POSTGRES_DB,
        )

    @staticmethod
    def load_from_env() -> "DatabaseSettings":
        return DatabaseSettings(
            POSTGRES_HOST=get_env_var("POSTGRES_HOST", to_cast=str, default="postgres"),
            POSTGRES_PORT=get_env_var("POSTGRES_PORT", to_cast=int, default=5432),
            POSTGRES_USER=get_env_var("POSTGRES_USER", to_cast=str),
            POSTGRES_PASSWORD=get_env_var("POSTGRES_PASSWORD", to_cast=str),
            POSTGRES_DB=get_env_var("POSTGRES_DB", to_cast=str),
        )


@dataclass(frozen=True)
class JwtSettings:

    PRIVATE_KEY: str
    PUBLIC_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    @staticmethod
    def load_from_env() -> "JwtSettings":
        return JwtSettings(
            PRIVATE_KEY=get_env_var(
                "PRIVATE_KEY",
                to_cast=str,
            ),
            PUBLIC_KEY=get_env_var(
                "PUBLIC_KEY",
                to_cast=str,
            ),
            ALGORITHM=get_env_var("ALGORITHM", to_cast=str, default="RS256"),
            ACCESS_TOKEN_EXPIRE_MINUTES=get_env_var(
                "ACCESS_TOKEN_EXPIRE_MINUTES",
                to_cast=int,
                default=15,
            ),
            REFRESH_TOKEN_EXPIRE_DAYS=get_env_var(
                "REFRESH_TOKEN_EXPIRE_DAYS",
                to_cast=int,
                default=30,
            ),
        )


@dataclass(frozen=True)
class SmtpSettings:

    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    FROM_EMAIL: str
    SENDER_NAME: str

    @staticmethod
    def load_from_env() -> "SmtpSettings":
        return SmtpSettings(
            HOST=get_env_var("SMTP_HOST", to_cast=str, default="smtp.yandex.ru"),
            PORT=get_env_var("SMTP_PORT", to_cast=int, default=465),
            USER=get_env_var("SMTP_EMAIL", to_cast=str),
            PASSWORD=get_env_var("SMTP_PASSWORD", to_cast=str),
            FROM_EMAIL=get_env_var("SMTP_EMAIL", to_cast=str),
            SENDER_NAME=get_env_var("SMTP_SENDER_NAME", to_cast=str),
        )


@dataclass(frozen=True)
class Settings:

    db: DatabaseSettings
    jwt: JwtSettings
    tochka: TochkaBankSettings
    smtp: SmtpSettings

    SESSION_MAX_AGE_DAYS: int

    DOMAIN_URL: str

    @staticmethod
    def load_from_env() -> "Settings":
        return Settings(
            db=DatabaseSettings.load_from_env(),
            jwt=JwtSettings.load_from_env(),
            tochka=TochkaBankSettings.load_from_env(),
            smtp=SmtpSettings.load_from_env(),
            SESSION_MAX_AGE_DAYS=get_env_var(
                "SESSION_MAX_AGE_DAYS",
                to_cast=int,
                default=30,
            ),
            DOMAIN_URL=get_env_var(
                "DOMAIN_URL",
                to_cast=str,
                default="https://localhost",
            ),
        )


settings = Settings.load_from_env()

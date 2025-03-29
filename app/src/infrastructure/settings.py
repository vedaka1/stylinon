from dataclasses import dataclass

from helpers import get_env_var


@dataclass(frozen=True)
class TochkaBankSettings:
    TOKEN: str
    PUBLIC_KEY: str
    ALGORITHM: str
    ACQUIRING_URL: str
    ACQUIRING_API_VERSION: str

    @staticmethod
    def load_from_env() -> 'TochkaBankSettings':
        return TochkaBankSettings(
            TOKEN=get_env_var('TOCHKA_TOKEN', str, default='working_token'),
            PUBLIC_KEY=get_env_var('ACQUIRING_PUBLIC_KEY', str),
            ALGORITHM=get_env_var('ACQUIRING_ALGORITHM', str, default='RS256'),
            ACQUIRING_URL=get_env_var('ACQUIRING_URL', str, default='https://enter.tochka.com/sandbox/v2'),
            ACQUIRING_API_VERSION=get_env_var('ACQUIRING_API_VERSION', str, default='v1.0'),
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
        return 'postgresql+asyncpg://{0}:{1}@{2}:{3}/{4}'.format(
            self.POSTGRES_USER,
            self.POSTGRES_PASSWORD,
            self.POSTGRES_HOST,
            self.POSTGRES_PORT,
            self.POSTGRES_DB,
        )

    @staticmethod
    def load_from_env() -> 'DatabaseSettings':
        return DatabaseSettings(
            POSTGRES_HOST=get_env_var('POSTGRES_HOST', str, default='postgres'),
            POSTGRES_PORT=get_env_var('POSTGRES_PORT', int, default=5432),
            POSTGRES_USER=get_env_var('POSTGRES_USER', str),
            POSTGRES_PASSWORD=get_env_var('POSTGRES_PASSWORD', str),
            POSTGRES_DB=get_env_var('POSTGRES_DB', str),
        )


@dataclass(frozen=True)
class JwtSettings:
    PRIVATE_KEY: str
    PUBLIC_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    @staticmethod
    def load_from_env() -> 'JwtSettings':
        return JwtSettings(
            PRIVATE_KEY=get_env_var(
                'PRIVATE_KEY',
                str,
            ),
            PUBLIC_KEY=get_env_var(
                'PUBLIC_KEY',
                str,
            ),
            ALGORITHM=get_env_var('ALGORITHM', str, default='RS256'),
            ACCESS_TOKEN_EXPIRE_MINUTES=get_env_var('ACCESS_TOKEN_EXPIRE_MINUTES', int, default=15),
            REFRESH_TOKEN_EXPIRE_DAYS=get_env_var('REFRESH_TOKEN_EXPIRE_DAYS', int, default=30),
        )


@dataclass(frozen=True)
class SmtpSettings:
    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    FROM_EMAIL: str
    SENDER_NAME: str
    ADMINISTRATOR_EMAIL: str

    @staticmethod
    def load_from_env() -> 'SmtpSettings':
        return SmtpSettings(
            HOST=get_env_var('SMTP_HOST', str, default='smtp.yandex.ru'),
            PORT=get_env_var('SMTP_PORT', int, default=465),
            USER=get_env_var('SMTP_EMAIL', str),
            PASSWORD=get_env_var('SMTP_PASSWORD', str),
            FROM_EMAIL=get_env_var('SMTP_EMAIL', str),
            SENDER_NAME=get_env_var('SMTP_SENDER_NAME', str),
            ADMINISTRATOR_EMAIL=get_env_var('SMTP_ADMINISTRATOR_EMAIL', str),
        )


@dataclass(frozen=True)
class Settings:
    db: DatabaseSettings
    jwt: JwtSettings
    acquiring: TochkaBankSettings
    smtp: SmtpSettings

    SESSION_MAX_AGE_DAYS: int

    DOMAIN_URL: str

    @staticmethod
    def load_from_env() -> 'Settings':
        return Settings(
            db=DatabaseSettings.load_from_env(),
            jwt=JwtSettings.load_from_env(),
            acquiring=TochkaBankSettings.load_from_env(),
            smtp=SmtpSettings.load_from_env(),
            SESSION_MAX_AGE_DAYS=get_env_var('SESSION_MAX_AGE_DAYS', int, default=30),
            DOMAIN_URL=get_env_var('DOMAIN_URL', str, default='https://localhost'),
        )


settings = Settings.load_from_env()

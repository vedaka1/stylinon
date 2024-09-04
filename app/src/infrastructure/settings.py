from src.infrastructure.utils.common import get_env_var


class DatabaseSettings:
    POSTGRES_HOST: str = get_env_var("POSTGRES_HOST", to_cast=str, default="postgres")
    POSTGRES_PORT: int = get_env_var("POSTGRES_PORT", to_cast=int, default=5432)
    POSTGRES_USER: str = get_env_var("POSTGRES_USER", to_cast=str)
    POSTGRES_PASSWORD: str = get_env_var("POSTGRES_PASSWORD", to_cast=str)
    POSTGRES_DB: str = get_env_var("POSTGRES_DB", to_cast=str)

    @property
    def DB_URL(self) -> str:
        return "postgresql+asyncpg://{0}:{1}@{2}:{3}/{4}".format(
            self.POSTGRES_USER,
            self.POSTGRES_PASSWORD,
            self.POSTGRES_HOST,
            self.POSTGRES_PORT,
            self.POSTGRES_DB,
        )


class JwtSettings:
    PRIVATE_KEY: str = get_env_var(
        "PRIVATE_KEY",
        to_cast=str,
    )
    PUBLIC_KEY: str = get_env_var(
        "PUBLIC_KEY",
        to_cast=str,
    )
    ALGORITHM: str = get_env_var("ALGORITHM", to_cast=str, default="RS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = get_env_var(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        to_cast=int,
        default=5,
    )
    REFRESH_TOKEN_EXPIRE_DAYS: int = get_env_var(
        "REFRESH_TOKEN_EXPIRE_DAYS",
        to_cast=int,
        default=30,
    )


class Settings:
    db: DatabaseSettings = DatabaseSettings()
    jwt: JwtSettings = JwtSettings()


settings = Settings()

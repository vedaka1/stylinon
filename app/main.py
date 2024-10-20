from contextlib import asynccontextmanager
from typing import AsyncGenerator

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.infrastructure.di.container import get_container, init_logger
from src.infrastructure.persistence.postgresql.database import get_async_engine
from src.presentation.api.v1.exc_handlers import init_exc_handlers
from src.presentation.api.v1.router import api_router as api_router_v1
from st_admin.main import init_admin


def init_di(app: FastAPI) -> None:
    container = get_container()
    setup_dishka(container, app)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    engine = get_async_engine()
    init_admin(app=app, engine=engine)
    yield
    await engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    api_v1 = FastAPI()
    init_di(api_v1)
    init_exc_handlers(api_v1)
    init_logger()
    api_v1.include_router(api_router_v1)
    api_v1.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost",
            "https://localhost",
            "http://vedaka.ru",
            "http://www.vedaka.ru",
            "https://vedaka.ru",
            "https://www.vedaka.ru",
            "https://merch.bank24.int",
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "HEAD", "OPTIONS", "PUT", "PATCH"],
        allow_headers=[
            "Access-Control-Allow-Headers",
            "Content-Type",
            "Authorization",
            "Cookies",
            "Access-Control-Allow-Origin",
        ],
    )
    app.mount("/api/v1", api_v1)
    return app

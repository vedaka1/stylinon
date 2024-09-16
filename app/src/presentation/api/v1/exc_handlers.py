import logging
from typing import cast

from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from src.application.common.response import ErrorAPIResponse
from src.domain.exceptions.base import ApplicationException
from starlette.types import ExceptionHandler

logger = logging.getLogger()


async def application_exception_handler(
    request: Request,
    exc: ApplicationException,
) -> ORJSONResponse:
    logger.error(msg="Handle error", exc_info=exc, extra={"error": exc})
    return ErrorAPIResponse(details=exc.message, status_code=exc.status_code)


async def unknown_exception_handler(
    request: Request,
    exc: Exception,
) -> ORJSONResponse:
    logger.error(msg="Handle error", exc_info=exc, extra={"error": exc})
    return ErrorAPIResponse(details="Unknown error occured", status_code=500)


def init_exc_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        ApplicationException,
        cast(ExceptionHandler, application_exception_handler),
    )
    app.add_exception_handler(
        Exception,
        cast(ExceptionHandler, unknown_exception_handler),
    )

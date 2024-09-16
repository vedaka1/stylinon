from dataclasses import dataclass, field
from re import T
from typing import Any, Generic, Mapping, TypeVar

from fastapi.responses import ORJSONResponse
from src.domain.exceptions.base import ApplicationException
from starlette.background import BackgroundTask

TData = TypeVar("TData")
TErrorData = TypeVar("TErrorData", bound=ApplicationException)


@dataclass
class APIResponse(Generic[TData]):
    ok: bool = True
    data: TData | dict[Any, Any] | list[Any] = field(default_factory=dict)


class ErrorAPIResponse(ORJSONResponse):
    def __init__(
        self,
        details: str = "Unknown error occured",
        status_code: int = 500,
        headers: Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None,
    ) -> None:
        content = {"ok": False, "error_code": status_code, "details": details}
        super().__init__(content, status_code, headers, media_type, background)

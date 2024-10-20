import os
from typing import Any, Callable
from uuid import uuid4

from fastapi import UploadFile


def cache_async_result(func: Callable[[], Any]) -> Any:
    cache: dict[str, Any] = {}

    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        key = func.__name__
        if key in cache:
            return cache[key]
        result: Any = await func(*args, **kwargs)
        cache[key] = result
        return result

    return wrapper


class StorageBackend:

    def __init__(self, path: str) -> None:
        self.path = path

    def _create_filename(self, file: UploadFile) -> str:
        content_type = "jpg"

        if file.filename:
            content_type = file.filename.split(".")[1]

        image_id = str(uuid4())

        file_name = f"{image_id}.{content_type}"

        return file_name

    def write(
        self,
        file: UploadFile,
        file_name: str | None = None,
    ) -> str:

        if not file_name:
            file_name = self._create_filename(file)

        with open(f"{self.path}/{file_name}", "wb+") as f:
            f.write(file.file.read())

        return f"{self.path}/{file_name}"

    def remove(self, file_name: str) -> None:
        os.remove(f"{self.path}/{file_name}")

    @property
    def default_image(self) -> str:
        return f"{self.path}/no_image.png"

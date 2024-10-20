from typing import Any, Dict
from uuid import uuid4

from fastapi import Request, UploadFile
from src.infrastructure.di.container import get_container
from src.infrastructure.utils.common import StorageBackend
from starlette_admin.contrib.sqla import ModelView


class UserView(ModelView):
    fields = [
        "id",
        "email",
        "hashed_password",
        "first_name",
        "last_name",
        "mobile_phone",
        "is_verified",
        "sessions",
        "role",
    ]

    name = "Пользователь"
    label = "Пользователи"
    exclude_fields_from_edit = ["id", "hashed_password", "sessions"]
    exclude_fields_from_create = ["id", "sessions"]

    async def before_create(
        self,
        request: Request,
        data: Dict[str, Any],
        obj: Any,
    ) -> None:
        container = get_container()
        storage_backend = await container.get(StorageBackend)
        image: UploadFile | None = data["image"][0]
        if image:
            image_path = storage_backend.write(file=image)
        else:
            image_path = "/images/no_image.png"
        data["image"] = image_path
        obj.id = uuid4()
        obj.image = image_path


class UserSessionsView(ModelView):
    label = "Сессии пользователей"

    searchable_fields = ["user"]

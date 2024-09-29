from typing import Any
from uuid import uuid4

from sqladmin import ModelView
from src.application.common.interfaces.password_hasher import PasswordHasherInterface
from src.infrastructure.di.container import get_container
from src.infrastructure.persistence.postgresql.models.user import UserModel


class UserAdmin(ModelView, model=UserModel):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"

    column_searchable_list = [
        UserModel.email,
        UserModel.first_name,
        UserModel.last_name,
        UserModel.mobile_phone,
    ]
    column_list = [
        UserModel.email,
        UserModel.first_name,
        UserModel.last_name,
        UserModel.mobile_phone,
        UserModel.role,
    ]
    column_labels = {
        "email": "Почта",
        "hashed_password": "Пароль",
        "first_name": "Имя",
        "last_name": "Фамилия",
        "mobile_phone": "Телефон",
        "role": "Роль",
        "is_verified": "Подтвержденый",
    }
    column_details_exclude_list = ["sessions"]
    form_excluded_columns = ["id", "sessions"]

    async def on_model_change(
        self,
        data: dict[str, Any],
        model: Any,
        is_created: bool,
        request: Any,
    ) -> None:
        if is_created:
            container = get_container()
            password_hasher = await container.get(PasswordHasherInterface)
            data["id"] = uuid4()
            data["hashed_password"] = password_hasher.hash(data["hashed_password"])

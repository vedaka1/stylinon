from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, Security
from src.application.common.response import APIResponse
from src.application.products.commands import CreateCategoryCommand
from src.application.products.usecases.create import CreateCategoryUseCase
from src.application.products.usecases.delete import DeleteCategoryUseCase
from src.application.products.usecases.get import GetCategoriesListUseCase
from src.domain.products.entities import Category
from src.domain.users.entities import UserRole
from src.presentation.dependencies.auth import get_current_user_data

router = APIRouter(tags=['Categories'], prefix='/categories', route_class=DishkaRoute)


@router.post(
    '',
    summary='Создает категорию',
    dependencies=[Security(get_current_user_data, scopes=[UserRole.ADMIN.value, UserRole.MANAGER.value])],
)
async def create_category(
    create_category_interactor: FromDishka[CreateCategoryUseCase],
    command: CreateCategoryCommand = Depends(),
) -> APIResponse[None]:
    await create_category_interactor.execute(command=command)
    return APIResponse()


@router.get('', summary='Возвращает список категорий')
async def get_categories(
    get_categories_list_interactor: FromDishka[GetCategoriesListUseCase],
) -> APIResponse[list[Category]]:
    response = await get_categories_list_interactor.execute()
    return APIResponse(data=response)


@router.delete(
    '/{category_name}',
    summary='Удаляет категорию по id',
    dependencies=[Security(get_current_user_data, scopes=[UserRole.ADMIN.value, UserRole.MANAGER.value])],
)
async def delete_category(
    category_name: str,
    delete_category_interactor: FromDishka[DeleteCategoryUseCase],
) -> APIResponse[None]:
    await delete_category_interactor.execute(category_name=category_name)

    return APIResponse()

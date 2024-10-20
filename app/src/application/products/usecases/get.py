from dataclasses import dataclass
from uuid import UUID

from src.application.common.pagination import ListPaginatedResponse, PaginationOutSchema
from src.application.products.commands import GetManyProductsCommand
from src.application.products.dto import ProductOut
from src.application.products.filters import ProductFilters
from src.domain.products.entities import Category
from src.domain.products.exceptions import ProductNotFoundException
from src.domain.products.repository import (
    CategoryRepositoryInterface,
    ProductRepositoryInterface,
)


@dataclass
class GetProductUseCase:

    product_repository: ProductRepositoryInterface

    async def execute(self, product_id: UUID) -> ProductOut:
        product = await self.product_repository.get_by_id(product_id=product_id)

        if not product:
            raise ProductNotFoundException

        return ProductOut(
            id=product.id,
            name=product.name,
            category=product.category,
            description=product.description,
            sku=product.sku,
            weight=product.weight,
            collection=product.collection,
            size=product.size,
            retail_price=product.retail_price,
            wholesale_price=product.d1_delivery_price,
            d1_delivery_price=product.d1_delivery_price,
            d1_self_pickup_price=product.d1_self_pickup_price,
            units_of_measurement=product.units_of_measurement,
            image=product.image,
            status=product.status,
            is_available=product.is_available,
        )


@dataclass
class GetManyProductsUseCase:

    product_repository: ProductRepositoryInterface

    async def execute(
        self,
        command: GetManyProductsCommand,
    ) -> ListPaginatedResponse[ProductOut]:
        filters = ProductFilters(
            name=command.name,
            category=command.category,
            description=command.description,
            units_of_measurement=command.units_of_measurement,
            price_from=command.price_from * 100 if command.price_from else None,
            price_to=command.price_to * 100 if command.price_to else None,
        )

        products = await self.product_repository.get_many(
            filters=filters,
            offset=command.pagination.offset,
            limit=command.pagination.limit,
        )

        total = await self.product_repository.count(filters=filters)

        return ListPaginatedResponse(
            items=[
                ProductOut(
                    id=product.id,
                    name=product.name,
                    category=product.category,
                    description=product.description,
                    sku=product.sku,
                    weight=product.weight,
                    collection=product.collection,
                    size=product.size,
                    retail_price=product.retail_price,
                    wholesale_price=product.d1_delivery_price,
                    d1_delivery_price=product.d1_delivery_price,
                    d1_self_pickup_price=product.d1_self_pickup_price,
                    units_of_measurement=product.units_of_measurement,
                    image=product.image,
                    status=product.status,
                    is_available=product.is_available,
                )
                for product in products
            ],
            pagination=PaginationOutSchema(
                limit=command.pagination.limit,
                page=command.pagination.page,
                total=total,
            ),
        )


@dataclass
class GetCategoriesListUseCase:

    category_repository: CategoryRepositoryInterface

    async def execute(self) -> list[Category]:
        categories = await self.category_repository.get_many()

        return categories

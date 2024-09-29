from dataclasses import dataclass
from uuid import UUID

from src.application.common.pagination import ListPaginatedResponse, PaginationOutSchema
from src.application.products.commands import (
    CreateProductCommand,
    GetManyProductsCommand,
)
from src.application.products.dto import ProductOut
from src.domain.products.entities import Product
from src.domain.products.service import ProductServiceInterface


@dataclass
class GetProductUseCase:
    product_service: ProductServiceInterface

    async def execute(self, product_id: UUID) -> ProductOut:
        product = await self.product_service.get_by_id(product_id=product_id)
        return ProductOut(
            id=product.id,
            name=product.name,
            category=product.category,
            description=product.description,
            price=product.price.value,
            units_of_measurement=product.units_of_measurement,
            photo_url=product.photo_url,
        )


@dataclass
class GetManyProductsUseCase:
    product_service: ProductServiceInterface

    async def execute(
        self,
        command: GetManyProductsCommand,
    ) -> ListPaginatedResponse[ProductOut]:
        products = await self.product_service.get_many(
            name=command.name,
            category=command.category,
            description=command.description,
            price_from=command.price_from,
            price_to=command.price_to,
            units_of_measurement=command.units_of_measurement,
            offset=command.pagination.offset,
            limit=command.pagination.limit,
        )
        total = await self.product_service.count(
            name=command.name,
            category=command.category,
            description=command.description,
            price_from=command.price_from,
            price_to=command.price_to,
            units_of_measurement=command.units_of_measurement,
        )
        return ListPaginatedResponse(
            items=[
                ProductOut(
                    id=product.id,
                    name=product.name,
                    category=product.category,
                    description=product.description,
                    price=product.price.value,
                    units_of_measurement=product.units_of_measurement,
                    photo_url=product.photo_url,
                )
                for product in products
            ],
            pagination=PaginationOutSchema(
                limit=command.pagination.limit,
                page=command.pagination.page,
                total=total,
            ),
        )

from dataclasses import dataclass
from uuid import UUID

from src.application.common.pagination import ListPaginatedResponse, PaginationOutSchema
from src.application.products.commands import GetManyProductsCommand
from src.application.products.dto import ProductOut, ProductVariantOut
from src.application.products.filters import ProductFilters
from src.domain.products.entities import Category
from src.domain.products.exceptions import ProductNotFoundException
from src.domain.products.repository import (
    CategoryRepositoryInterface,
    ProductRepositoryInterface,
)
from src.domain.products.value_objects import ProductPrice


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
            units_of_measurement=product.units_of_measurement,
            variants=[
                ProductVariantOut(
                    id=variant.id,
                    name=variant.name,
                    sku=variant.sku,
                    bag_weight=variant.bag_weight,
                    pallet_weight=variant.pallet_weight,
                    bags_per_pallet=variant.bags_per_pallet,
                    retail_price=ProductPrice(variant.retail_price.value).in_rubles(),
                    wholesale_delivery_price=ProductPrice(
                        variant.wholesale_delivery_price.value,
                    ).in_rubles(),
                    d2_delivery_price=ProductPrice(
                        variant.d2_delivery_price.value,
                    ).in_rubles(),
                    d2_self_pickup_price=ProductPrice(
                        variant.d2_self_pickup_price.value,
                    ).in_rubles(),
                    d1_delivery_price=ProductPrice(
                        variant.d1_delivery_price.value,
                    ).in_rubles(),
                    d1_self_pickup_price=ProductPrice(
                        variant.d1_self_pickup_price.value,
                    ).in_rubles(),
                    image=variant.image,
                    status=product.status,
                )
                for variant in product.product_variants
            ],
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
            price_from=command.price_from,
            price_to=command.price_to,
        )

        products = await self.product_repository.get_many(
            filters=filters,
            offset=command.pagination.offset,
            limit=command.pagination.limit,
            with_relations=True,
        )

        total = await self.product_repository.count(filters=filters)

        return ListPaginatedResponse(
            items=[
                ProductOut(
                    id=product.id,
                    name=product.name,
                    category=product.category,
                    description=product.description,
                    units_of_measurement=product.units_of_measurement,
                    variants=[
                        ProductVariantOut(
                            id=variant.id,
                            name=variant.name,
                            sku=variant.sku,
                            bag_weight=variant.bag_weight,
                            pallet_weight=variant.pallet_weight,
                            bags_per_pallet=variant.bags_per_pallet,
                            image=variant.image,
                            retail_price=ProductPrice(
                                variant.retail_price.value,
                            ).in_rubles(),
                            wholesale_delivery_price=ProductPrice(
                                variant.wholesale_delivery_price.value,
                            ).in_rubles(),
                            d2_delivery_price=ProductPrice(
                                variant.d2_delivery_price.value,
                            ).in_rubles(),
                            d2_self_pickup_price=ProductPrice(
                                variant.d2_self_pickup_price.value,
                            ).in_rubles(),
                            d1_delivery_price=ProductPrice(
                                variant.d1_delivery_price.value,
                            ).in_rubles(),
                            d1_self_pickup_price=ProductPrice(
                                variant.d1_self_pickup_price.value,
                            ).in_rubles(),
                            status=variant.status,
                        )
                        for variant in product.product_variants
                    ],
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

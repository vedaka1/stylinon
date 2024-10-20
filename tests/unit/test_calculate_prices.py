import pytest
from src.application.common.utils import parse_price
from src.application.orders.utils import calculate_product_price
from src.application.products.dto import PaymentMethod
from src.domain.products.entities import Product, ProductStatus
from src.domain.products.value_objects import ProductPrice

test_params_1 = ()


def create_product(
    retail_price: int,
    wholesale_price: int | None = None,
    d1_self_pickup_price: int | None = None,
    d1_delivery_price: int | None = None,
) -> Product:
    return Product.create(
        category="test_category",
        description="test_description",
        name="test_product_variant",
        sku="test_sku",
        weight=10,
        retail_price=ProductPrice(retail_price),
        wholesale_price=parse_price(wholesale_price),
        d1_self_pickup_price=parse_price(d1_self_pickup_price),
        d1_delivery_price=parse_price(d1_delivery_price),
        status=ProductStatus.AVAILABLE,
    )


@pytest.mark.parametrize(
    "product, payment_method, is_self_pickup, order_weight, products_count, expected",
    [
        # 1. Рынок: вес <= 20 тонн, ожидаемая цена по умолчанию
        (
            create_product(retail_price=1000),
            PaymentMethod.FULL_PREPAYMENT,
            False,
            15000,
            1,
            1000,
        ),
        # 2. Один товар, вес > 20 тонн, оптовая доставка
        (
            create_product(retail_price=1000, wholesale_price=800),
            PaymentMethod.FULL_PREPAYMENT,
            False,
            21000,
            1,
            800,
        ),
        # 3. Один товар, вес > 20 тонн, без оптовой доставки
        (
            create_product(retail_price=1000, wholesale_price=None),
            PaymentMethod.FULL_PREPAYMENT,
            False,
            21000,
            1,
            1000,
        ),
        # 4. Предоплата, самовывоз, вес > 20 тонн, цена самовывоза
        (
            create_product(
                retail_price=1000,
                d1_self_pickup_price=900,
                d1_delivery_price=950,
            ),
            PaymentMethod.FULL_PREPAYMENT,
            True,
            25000,
            1,
            900,
        ),
        # 5. Предоплата, доставка, вес > 20 тонн
        (
            create_product(
                retail_price=1000,
                d1_self_pickup_price=None,
                d1_delivery_price=950,
            ),
            PaymentMethod.FULL_PREPAYMENT,
            False,
            25000,
            1,
            950,
        ),
        # 6. Несколько товаров, вес > 20 тонн
        (
            create_product(retail_price=1000),
            PaymentMethod.FULL_PREPAYMENT,
            False,
            25000,
            5,
            1000,
        ),
        # 7. Вес равен 20 тоннам, проверка обычной цены
        (
            create_product(retail_price=1000),
            PaymentMethod.FULL_PREPAYMENT,
            False,
            20000,
            1,
            1000,
        ),
    ],
)
def test_calculate_product_price(
    product: Product,
    payment_method: PaymentMethod,
    is_self_pickup: bool,
    order_weight: int,
    products_count: int,
    expected: int,
) -> None:
    price = calculate_product_price(
        product=product,
        payment_method=payment_method,
        is_self_pickup=is_self_pickup,
        order_weight=order_weight,
        products_count=products_count,
    )

    assert price == expected

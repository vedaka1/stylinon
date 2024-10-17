from src.domain.products.value_objects import ProductPrice


def convert_price(price: ProductPrice | None) -> float | None:
    return price.in_rubles() if price else None


def parse_price(price: int | None) -> ProductPrice | None:
    return ProductPrice(price) if price else None

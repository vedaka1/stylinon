from dataclasses import dataclass

from src.domain.products.exceptions import ProductIncorrectPriceException


@dataclass
class ProductPrice:
    value: int

    def __post_init__(self) -> None:
        if not isinstance(self.value, int):
            raise ValueError('Value must be a integer')
        if self.value <= 0:
            raise ProductIncorrectPriceException

    def in_rubles(self) -> float:
        return self.value / 100

    @staticmethod
    def from_rubles(value: int) -> 'ProductPrice':
        value *= 100
        return ProductPrice(value)

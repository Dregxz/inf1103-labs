from typing import List, Optional
from product import Product
from order_line import OrderLine
from discount_strategy import DiscountStrategy, NoDiscount


class Order:
    """Represents a customer order composed of OrderLine items and using a DiscountStrategy."""

    def __init__(self, order_id: str, discount: Optional[DiscountStrategy] = None) -> None:
        self.__order_id: str = order_id
        self.order_lines: List[OrderLine] = []
        self.discount: DiscountStrategy = discount if discount is not None else NoDiscount()

    def get_order_id(self) -> str:
        return self.__order_id

    def get_discount(self) -> DiscountStrategy:
        return self.discount

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.discount = discount

    def add_line(self, product: Product, quantity: int) -> OrderLine:
        line = OrderLine(product, quantity)
        self.order_lines.append(line)
        return line

    def calculate_total(self) -> float:
        total = sum(line.calculate_subtotal() for line in self.order_lines)
        return self.discount.apply(total)

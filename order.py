from typing import List
from product import Product
from order_line import OrderLine


class Order:
    """Represents a customer order composed of OrderLine items."""

    def __init__(self, order_id: str) -> None:
        self.__order_id: str = order_id
        self.order_lines: List[OrderLine] = []

    def get_order_id(self) -> str:
        return self.__order_id

    def add_line(self, product: Product, quantity: int) -> OrderLine:
        line = OrderLine(product, quantity)
        self.order_lines.append(line)
        return line

    def calculate_total(self) -> float:
        return sum(line.calculate_subtotal() for line in self.order_lines)

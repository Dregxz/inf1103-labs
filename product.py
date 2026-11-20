from abc import ABC, abstractmethod
from typing import Optional
from supplier import Supplier


class Product(ABC):
    """Abstract base class representing a product in the inventory."""

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Optional[Supplier] = None,
    ) -> None:
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = float(price)
        self.__stock: int = int(stock)
        self.__supplier: Optional[Supplier] = supplier

    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def get_supplier(self) -> Optional[Supplier]:
        return self.__supplier

    def update_stock(self, quantity: int) -> bool:
        if isinstance(quantity, int) and quantity >= 0:
            self.__stock = quantity
            return True
        return False

    def display_information(self) -> None:
        supplier_info = f" | Supplier: {self.__supplier.get_name()}" if self.__supplier else ""
        print(
            f"ID: {self.__product_id} | Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | Stock: {self.__stock}{supplier_info}"
        )

    def to_dict(self) -> dict:
        """Common data every product saves. Subclasses extend this."""
        return {
            "Name": self.__name,
            "Price": self.__price,
            "Stock": self.__stock,
        }

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Each product type must say how it is fulfilled."""
        pass

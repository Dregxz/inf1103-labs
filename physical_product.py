from typing import Optional
from product import Product
from can_be_shipped import CanBeShipped
from supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):

    BASE_SHIPPING_FEE: float = 5.00   # flat fee in dollars
    RATE_PER_KG: float = 2.00         # dollars per kilogram

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Optional[Supplier] = None,
        weight: float = 0.0,
    ) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight: float = float(weight)

    def get_weight(self) -> float:
        return self.__weight

    def display_information(self) -> None:
        super().display_information()
        print(f"    Weight: {self.__weight:.2f} kg")

    def get_fulfilment_info(self) -> str:
        return "Physical product: requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        return self.BASE_SHIPPING_FEE + self.RATE_PER_KG * self.__weight

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["Type"] = "physical"
        data["Weight"] = self.__weight
        return data

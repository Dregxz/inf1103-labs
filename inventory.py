from typing import List, Optional
from product import Product


class Inventory:
    """Manages a collection of Product objects."""

    def __init__(self) -> None:
        self.__products: List[Product] = []

    def add_product(self, product: Product) -> bool:
        if self.search_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def search_product(self, product_id: str) -> Optional[Product]:
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def display_all(self) -> None:
        if not self.__products:
            print("No products in inventory.")
            return
        for product in self.__products:
            product.display_information()

    def get_all_products(self) -> List[Product]:
        return list(self.__products)

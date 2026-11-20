from typing import Optional
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier


class ProductFactory:
    """Centralises creation of concrete Product subclasses."""

    @staticmethod
    def create(
        product_type: str,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        supplier: Optional[Supplier] = None,
        weight: float = 0.0,
        download_size: float = 0.0,
    ) -> Product:
        normalized = product_type.strip().lower()
        if normalized == "physical":
            return PhysicalProduct(
                product_id, name, price, stock_quantity, supplier, weight=weight
            )
        elif normalized == "digital":
            return DigitalProduct(
                product_id,
                name,
                price,
                stock_quantity,
                supplier,
                download_size=download_size,
            )
        else:
            raise ValueError(f"Unknown product type: {product_type}")

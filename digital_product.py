from typing import Optional
from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Optional[Supplier] = None,
        download_size: float = 0.0,
    ) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__download_size: float = float(download_size)

    def get_download_size(self) -> float:
        return self.__download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"    Download size: {self.__download_size:.2f} MB")

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["Type"] = "digital"
        data["Download Size"] = self.__download_size
        return data

    def get_fulfilment_info(self) -> str:
        return "Digital product: delivered digitally via download link."

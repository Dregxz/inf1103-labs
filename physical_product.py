from product import Product
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    BASE_SHIPPING_COST = 5.0  
    Rate_PER_KG = 2.0
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = float(weight)

    def get_weight(self):
        return self.__weight

    def display_information(self):
        super().display_information()
        print(f"    Weight: {self.__weight:.2f} kg")

    def calculate_shipping_cost(self):
        return self.BASE_SHIPPING_COST + self.Rate_PER_KG * self.__weight

    def to_dict(self):
        data = super().to_dict()
        data["Type"] = "Physical"
        data["Weight"] = self.__weight
        return data

    def get_fulfilment_info(self):
        return "Physical product: requires physical shipping."

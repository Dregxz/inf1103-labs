class Product:
    
    def __init__(self, ID, name, price, stock):
        self.__ID = ID
        self.__name = name
        self.__price = price
        self.stock = stock

    def get_product_id(self):
        return self.__ID

    def get_product_name(self):
        return self.__name

    def get_product_price(self):
        return self.__price

    def get_product_stock(self):
        return self.__stock

    def update_stock(self, new_stock):
        if isinstance(new_stock, int) and new_stock >= 0:
            self.stock = new_stock
            return True
        return False

    def display_product(self):
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock}")
        
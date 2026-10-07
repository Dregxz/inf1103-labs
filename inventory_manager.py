import json
option = int
inventory_dict={}

Menufile = "inventory.json"

def print_line():
    print("----------------------------------")

def get_valid_input(datain):
    global items
    if datain.isdigit() or datain == ("quit"):
        return datain

def process_delivery(current_total, new_value):
    if new_value.isdigit():
        return current_total+int(new_value)
    else :
        return current_total

def calculate_tax(amount):
    amount=amount*3 #delivery amount
    return amount*0.1

def generate_report(total_unit, failed_attempt):
    print("Total Unit Processed: ", total_unit)
    print("Rejected Entry: ", failed_attempt) 

def load_inventory():
    with open("inventory.txt", "r") as file:
            print(file.read())
    with open("inventory.txt", "r") as file:
        return file.read().splitlines()

def save_inventory(orders):
    with open("inventory.txt", "w") as file:
        for item in orders:
            file.write(f"{item}\n")

def add_product():
    print("Add New Product")
    ID = input("Product ID: ")
    get_valid_input(ID)
    productName = input("Product Name: ")
    price = input("Price: ")
    get_valid_input(price)
    if isinstance(price, float) or price.isdigit:
        stock = input("Stock Quantity: ")
        get_valid_input(stock)
        if stock.isdigit():
            inventory_dict = {"Name" : productName,
                              "Price": price,
                              "Stock": stock
                              }
            try:
                with open("inventory.json", "r") as file:
                    datalist=json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                    datalist={"": []}
            
            if "" in datalist:
                del datalist[""]
                
            datalist[ID] = inventory_dict
            
            with open("inventory.json", "w") as file:
                json.dump(datalist, file, indent=4)

    else:
        print("Rejected!")



def update_stock(datain, dataout):
    with open(Menufile, "r") as file:
        print()

def search_product(datain):
    with open(Menufile, "r") as file:
        print()

def display_all():

    with open(Menufile, "r") as file:
        products=json.load(file)
        for pid, details in products.items():
            name = details["Name"]
            price = float(details["Price"])
            stk = details["Stock"]

            print("Current Inventory")
            print_line()
            print(f"ID: {pid:} | Name: {name:} | Price: ${price:.2f} | Stock: {stk:}")
            print_line()


print("--------MENU--------")
print("1. Display All Products")
print("2. Add product")
print("3. Update Stock")
print("4. Search Product")
print("5. Save Inventory")
print("6. Exit")
print("\n")

while option != "6":
    option = input("Enter option: ")
    get_valid_input(option)
    print("\n")

    if option == "1":
        print_line()
        display_all()

    elif option == "2":
        add_product()
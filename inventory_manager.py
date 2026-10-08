import json
option = int
Menufile = "inventory.json"

def print_line1():
    print("----------------------------------")

def print_line2():
    print("=======================================")

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

def user_input():
    ID = input("Product ID: ")
    productName = input("Product Name: ")
    price = input("Price: ")
    get_valid_input(price)
    if isinstance(price, float) or price.isdigit:
        stock = input("Stock Quantity: ")
        get_valid_input(stock)
        if stock.isdigit():
            dataout = {"Name" : productName,
                        "Price": price,                               
                        "Stock": stock
                        }
            return ID, dataout
        
def add_product(IDin, datain):
    if IDin != 0:
        if "" in datalist:
            del datalist[""]

        else:
            datalist[IDin] = datain
            
        return datalist         

    else:
        print("Rejected!")

def update_stock():
    
    IDin = input("Enter Product ID: ")
    print("\n")
    if IDin in datalist:
        print("Product Found")
        name = datalist[IDin]["Name"]
        price = float(datalist[IDin]["Price"])
        print("Name: ", name)
        print("Price: ", price, "\n")
        datalist[IDin]["Stock"] = input("New Stock Quantity: ")
        print("Item Updated")

        return datalist     

    else:
        print("Item not found")

def search_product():
    searchID=input("Enter Product ID: ")

    if searchID in datalist:
        name = datalist[searchID]["Name"]
        price = float(datalist[searchID]["Price"])
        stk = datalist[searchID]["Stock"]
        print("Product Found")
        print_line1()
        print(f"ID: {searchID:}\nName: {name:}\nPrice: ${price:.2f}\nStock: {stk:}")
        print_line1()

    else:
        print("Product not Found")

def display_all():       
    if "" in datalist:
        print("No Entry")

    else:        
        for pid, details in datalist.items():
            name = details["Name"]
            price = float(details["Price"])
            stk = details["Stock"]
            print(f"ID: {pid:} | Name: {name:} | Price: ${price:.2f} | Stock: {stk:}")

print_line2()
print("INVENTORY MANAGEMENT SYSTEM")
print_line2()
print("\n")

try:
    with open("inventory.json", "r") as file:
        print("inventory.json found.")
        datalist=json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    datalist={"": []}

print("Inventory loaded successfully.\n")    
print("--------MENU--------")
print("1. Display All Products")
print("2. Add product")
print("3. Update Stock")
print("4. Search Product")
print("5. Save Inventory")
print("6. Exit")
print("---------------------")

while option != "6":
    option = input("\nEnter option: ")
    get_valid_input(option)

    if option == "1":
        print("Current Inventory")
        print_line1()
        display_all()
        print_line1()
        print("\n")

    elif option == "2":
        
        print("Add New Product\n")
        ID,data=user_input()
        datalist = add_product(ID, data)
        print("\nProduct added Successfully!\n")
        
    elif option == "3":
        print("Update Product\n")
        datalist = update_stock()
        print("\n")

    elif option == "4":
        search_product()
        print("\n")

    elif option == "5":
        print("Saving Inventory...")
        if datalist != {}:
            datalist=dict(sorted(datalist.items()))
            with open("inventory.json", "w") as file:
              json.dump(datalist, file, indent=4)    
        print("Inventory saved Successfully to inventiry.json.")

    elif option == "6":
        print("Saving Inventory before exit...")
        if datalist != {}:
            datalist=dict(sorted(datalist.items()))
            with open("inventory.json", "w") as file:
                json.dump(datalist, file, indent=4)
        print("Inventory saved Successfully.\n")
        print("Thank you for using Inventory Management System.\nProgram terminated.")
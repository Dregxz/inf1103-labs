inventory = 0
items = ["Wireless Mouse","Keyboard","USB Cable","Laptop Stand"]
stock = str 
product = str
error = 0
totaltax=0
current_orders = list

def get_valid_input(inv):
    if inv.isdigit() or inv == ("quit") or inv in items:
        return inv

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

current_orders=load_inventory()
#current_orders.append("1")
save_inventory(current_orders)
while stock != ("quit"):
    product = (input("Enter Product Name: "))
    get_valid_input(product)
    stock = (input("Enter Quantity: "))
    get_valid_input(stock)

    inventory = process_delivery(inventory, stock)
    if stock.isdigit():
        tax=+calculate_tax(int(stock))
        print("$",round(tax, 3))
        totaltax+=tax

    elif stock != ("quit"):
        print("Rejected!")
        error+=1

generate_report(inventory, error)
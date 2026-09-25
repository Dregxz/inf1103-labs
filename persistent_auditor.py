inventory = 0
items = ["Wireless Mouse","Keyboard","USB Cable","Laptop Stand"]
codes = ["1001","1002","1003","1004"]
ordered_items = dict(zip(items, codes))
stock = str 
product = str
error = 0
current_orders = list
added_items = str

def get_valid_input(inv):
    global items
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



while stock != ("quit") or product!=(quit):
    current_orders=load_inventory()
    product = (input("Enter Product Name: "))
    get_valid_input(product)

    if product != ("quit") and product in items:
        stock = (input("Enter Quantity: "))
        get_valid_input(stock)

        if stock.isdigit():
            added_items=({v for k, v in ordered_items.items() if product in k}, product, stock)

    elif product == ("quit"):
        break
    
    else:
        print("Rejected!")
        error+=1


    
    current_orders.append(added_items)
    save_inventory(current_orders)

    

generate_report(inventory, error)
#writing into file works
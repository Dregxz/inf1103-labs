inventory = 0
stock = ("")
error = 0

def get_valid_input(inv):
    if inv.isdigit() or inv == ("quit"):
        return inv

def process_delivery(current_total, new_total):
    if current_total.isdigit():
        new_total+=int(current_total)
        return new_total



while stock != ("quit"):
    stock = (input("Enter value: "))
    get_valid_input(stock)
    process_delivery(stock, inventory)


    

print("Total Unit Processed: ", inventory)
print("Rejected Entry: ", error) 
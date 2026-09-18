inventory = 0
order = str 
error = 0

def get_valid_input(inv):
    if inv.isdigit() or inv == ("quit"):
        return inv

def process_delivery(current_total, new_total):
    if current_total.isdigit():
        return new_total+int(current_total)
    else :
        return new_total


while order != ("quit"):
    order = (input("Enter value: "))
    get_valid_input(order)
    inventory = process_delivery(order, inventory)

print("Total Unit Processed: ", inventory)
print("Rejected Entry: ", error) 
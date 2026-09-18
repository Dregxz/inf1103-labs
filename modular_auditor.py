inventory = 0
stock = str 
error = 0
totaltax=0

def get_valid_input(inv):
    if inv.isdigit() or inv == ("quit"):
        return inv

def process_delivery(current_total, new_value):
    if new_value.isdigit():
        return current_total+int(new_value)
    else :
        return current_total

def calculate_tax(amount):
    amount=amount*3 #delivery amount
    return amount*0.1

def generate_report(total_unit, failed_attempt, taxes):
    print("Total Unit Processed: ", total_unit)
    print("Rejected Entry: ", failed_attempt) 
    print("Total Tax: $", round(taxes,3))

while stock != ("quit"):
    stock = (input("Enter value: "))
    get_valid_input(stock)
    inventory = process_delivery(inventory, stock)
    if stock.isdigit():
        tax=+calculate_tax(int(stock))
        print("$",round(tax, 3))
        totaltax+=tax

    elif stock != ("quit"):
        error=+1

generate_report(inventory, error, totaltax)
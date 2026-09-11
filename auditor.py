inventory = 0
error = 0

while inventory <= 500:
    stock = (input("Enter value: "))

    if stock == "quit" or stock=="Quit":
        break 

    elif stock.isdigit():
        inventory += int(stock)

    else:
        print("Rejected")
        error +=1

if inventory >500:
    print("Too Full")

else:
        print("Total Unit Processed: ", inventory)
        print("Rejected Entry: ", error) 


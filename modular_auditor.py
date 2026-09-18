inventory = 0
stock = ("")
error = 0

while stock != ("quit"):
    stock = (input("Enter value: "))

    if stock.isdigit():
        inventory += int(stock)

        if inventory >500:
             print ("Too Full!")
             break

    elif stock !=("quit"):
        print("Rejected")
        error +=1

print("Total Unit Processed: ", inventory)
print("Rejected Entry: ", error) 
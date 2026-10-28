import json
from product import Product
from inventory import Inventory

FILENAME = "inventory.json"


def print_line1():
    print("----------------------------------")


def print_line2():
    print("=======================================")


def load_inventory(inventory):
    try:
        with open(FILENAME, "r") as file:
            data = json.load(file)
        print(f"{FILENAME} found.")
        for product_id, details in data.items():
            try:
                product = Product(product_id, details["Name"],
                                  details["Price"], details["Stock"])
                inventory.add_product(product)
            except (KeyError, ValueError, TypeError):
                print(f"Skipped invalid entry: {product_id!r}")
    except (FileNotFoundError, json.JSONDecodeError):
        print("No valid inventory file found. Starting with an empty inventory.")


def save_inventory(inventory):
    data = {}
    for product in inventory.get_all_products():
        data[product.get_product_id()] = {
            "Name": product.get_name(),
            "Price": product.get_price(),
            "Stock": product.get_stock(),
        }
    data = dict(sorted(data.items()))
    with open(FILENAME, "w") as file:
        json.dump(data, file, indent=4)


def ask_float(prompt):
    try:
        value = float(input(prompt))
        return value if value >= 0 else None
    except ValueError:
        return None


def ask_int(prompt):
    value = input(prompt)
    return int(value) if value.isdigit() else None


def add_product_menu(inventory):
    print("Add New Product\n")
    product_id = input("Product ID: ").strip()
    name = input("Product Name: ").strip()
    if not product_id or not name:
        print("Rejected! ID and name cannot be empty.")
        return
    price = ask_float("Price: ")
    if price is None:
        print("Rejected! Price must be a non-negative number.")
        return
    stock = ask_int("Stock Quantity: ")
    if stock is None:
        print("Rejected! Stock must be a whole number.")
        return

    product = Product(product_id, name, price, stock)
    if inventory.add_product(product):
        print("\nProduct added Successfully!")
    else:
        print("Rejected! That Product ID already exists.")


def update_stock_menu(inventory):
    print("Update Product\n")
    product = inventory.search_product(input("Enter Product ID: ").strip())
    if product is None:
        print("Item not found")
        return
    print("Product Found")
    product.display_information()
    new_stock = ask_int("New Stock Quantity: ")
    if new_stock is not None and product.update_stock(new_stock):
        print("Item Updated")
    else:
        print("Rejected! Stock must be a whole number.")


def search_product_menu(inventory):
    product = inventory.search_product(input("Enter Product ID: ").strip())
    if product is None:
        print("Product not Found")
    else:
        print("Product Found")
        print_line1()
        product.display_information()
        print_line1()


def print_menu():
    print("--------MENU--------")
    print("1. Display All Products")
    print("2. Add product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("---------------------")


def main():
    print_line2()
    print("INVENTORY MANAGEMENT SYSTEM")
    print_line2()

    inventory = Inventory()
    load_inventory(inventory)
    print("Inventory loaded successfully.\n")
    print_menu()

    option = ""
    while option != "6":
        option = input("\nEnter option: ").strip()

        if option == "1":
            print("Current Inventory")
            print_line1()
            inventory.display_all()
            print_line1()
        elif option == "2":
            add_product_menu(inventory)
        elif option == "3":
            update_stock_menu(inventory)
        elif option == "4":
            search_product_menu(inventory)
        elif option == "5":
            save_inventory(inventory)
            print(f"Inventory saved Successfully to {FILENAME}.")
        elif option == "6":
            print("Saving Inventory before exit...")
            save_inventory(inventory)
            print("Inventory saved Successfully.\n")
            print("Thank you for using Inventory Management System.\nProgram terminated.")
        else:
            print("Invalid option. Please enter 1-6.")


if __name__ == "__main__":
    main()
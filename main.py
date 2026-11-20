import csv
import json
from typing import Optional
from inventory import Inventory
from supplier import Supplier
from can_be_shipped import CanBeShipped
from product_factory import ProductFactory
from order import Order
from discount_strategy import (
    DiscountStrategy,
    NoDiscount,
    PercentageDiscount,
    BulkDiscount,
    StudentDiscount,
)

FILENAME = "inventory.json"
CSV_FILENAME = "products.csv"


def print_line1() -> None:
    print("----------------------------------")


def print_line2() -> None:
    print("=======================================")


def get_positive_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def get_non_negative_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Please enter a non-negative number.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 1.50")


def get_non_negative_int(prompt: str) -> int:
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Please enter a whole number (0 or greater).")
                continue
            return value
        except ValueError:
            print("Please enter a valid whole number, e.g. 10")


def get_positive_int(prompt: str) -> int:
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Please enter a whole number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid whole number, e.g. 2")


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        loaded = 0
        with file:
            reader = csv.reader(file)
            next(reader, None)  # skip header row
            for row_num, row in enumerate(reader, start=2):
                if not row:
                    continue
                try:
                    product_type, product_id, name, price_str, stock_str = row
                    product = ProductFactory.create(
                        product_type=product_type,
                        product_id=product_id.strip(),
                        name=name.strip(),
                        price=float(price_str),
                        stock_quantity=int(stock_str),
                        supplier=supplier,
                    )
                    if inventory.add_product(product):
                        loaded += 1
                    else:
                        print(f"Row {row_num} skipped: duplicate Product ID '{product_id.strip()}'.")
                except ValueError as exc:
                    print(f"Row {row_num} skipped: {exc}")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")


def load_inventory(inventory: Inventory, supplier: Optional[Supplier] = None) -> None:
    try:
        with open(FILENAME, "r") as file:
            data = json.load(file)
        print(f"{FILENAME} found.")
        for product_id, details in data.items():
            try:
                product_type = details.get("Type", "physical")
                product = ProductFactory.create(
                    product_type=product_type,
                    product_id=product_id,
                    name=details["Name"],
                    price=float(details["Price"]),
                    stock_quantity=int(details["Stock"]),
                    supplier=supplier,
                    weight=float(details.get("Weight", 0.0)),
                    download_size=float(
                        details.get("Download Size", details.get("Download_Size", 0.0))
                    ),
                )
                inventory.add_product(product)
            except (KeyError, ValueError, TypeError):
                print(f"Skipped invalid entry: {product_id!r}")
    except (FileNotFoundError, json.JSONDecodeError):
        print("No valid inventory file found. Starting with an empty inventory.")


def save_inventory(inventory: Inventory) -> None:
    data = {}
    for product in inventory.get_all_products():
        data[product.get_product_id()] = product.to_dict()
    data = dict(sorted(data.items()))
    with open(FILENAME, "w") as file:
        json.dump(data, file, indent=4)


def add_product_menu(inventory: Inventory, supplier: Optional[Supplier] = None) -> None:
    print("Add New Product\n")
    product_id = input("Product ID: ").strip()
    name = input("Product Name: ").strip()
    if not product_id or not name:
        print("Rejected! ID and name cannot be empty.")
        return

    price = get_positive_float("Price: ")
    stock = get_non_negative_int("Stock Quantity: ")

    print("\nProduct type:")
    print("1. Physical product")
    print("2. Digital product")
    choice = input("Choose type (1-2): ").strip()

    weight = 0.0
    download_size = 0.0
    if choice == "1":
        product_type = "physical"
        weight = get_non_negative_float("Weight (kg): ")
    elif choice == "2":
        product_type = "digital"
        download_size = get_non_negative_float("Download size (MB): ")
    else:
        print("Rejected! Product type must be 1 or 2.")
        return

    try:
        product = ProductFactory.create(
            product_type=product_type,
            product_id=product_id,
            name=name,
            price=price,
            stock_quantity=stock,
            supplier=supplier,
            weight=weight,
            download_size=download_size,
        )
    except ValueError as exc:
        print(f"Rejected! {exc}")
        return

    if inventory.add_product(product):
        print("\nProduct added Successfully!")
    else:
        print("Rejected! That Product ID already exists.")


def update_stock_menu(inventory: Inventory) -> None:
    print("Update Product\n")
    product = inventory.search_product(input("Enter Product ID: ").strip())
    if product is None:
        print("Item not found")
        return
    print("Product Found")
    product.display_information()
    new_stock = get_non_negative_int("New Stock Quantity: ")
    try:
        product.update_stock(new_stock)
        print("Item Updated")
    except ValueError as exc:
        print(f"Rejected! {exc}")


def search_product_menu(inventory: Inventory) -> None:
    product = inventory.search_product(input("Enter Product ID: ").strip())
    if product is None:
        print("Product not Found")
    else:
        print("Product Found")
        print_line1()
        product.display_information()
        print(f"    {product.get_fulfilment_info()}")
        if isinstance(product, CanBeShipped):
            print(f"    Shipping cost: ${product.calculate_shipping_cost():.2f}")
        print_line1()


def create_order_menu(inventory: Inventory) -> None:
    print("Create Customer Order\n")
    order_id = input("Order ID: ").strip() or "ORD001"
    order = Order(order_id)

    while True:
        pid = input("Enter Product ID to add (or 'done' to finish): ").strip()
        if pid.lower() == "done":
            break
        product = inventory.search_product(pid)
        if product is None:
            print("Product not found.")
            continue
        qty = get_positive_int("Quantity: ")
        try:
            order.add_line(product, qty)
            print(f"Added {qty} x {product.get_name()}.")
        except ValueError as exc:
            print(f"Rejected! {exc}")

    if not order.order_lines:
        print("Order cancelled (no items added).")
        return

    print("\nSelect Discount Strategy:")
    print("1. No Discount")
    print("2. 10% Percentage Discount")
    print("3. Bulk Discount ($20 off orders >= $200)")
    print("4. Student Discount (5% off)")
    d_choice = input("Choose discount (1-4): ").strip()

    strategy_map: dict[str, DiscountStrategy] = {
        "1": NoDiscount(),
        "2": PercentageDiscount(10),
        "3": BulkDiscount(200, 20),
        "4": StudentDiscount(),
    }
    order.set_discount(strategy_map.get(d_choice, NoDiscount()))
    print_line1()
    print(f"Order {order.get_order_id()} Final Total: ${order.calculate_total():.2f}")
    print_line1()


def print_menu() -> None:
    print("--------MENU--------")
    print("1. Display All Products")
    print("2. Add product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Load Products from CSV")
    print("7. Create Order with Discount")
    print("8. Exit")
    print("---------------------")


def main() -> None:
    print_line2()
    print("INVENTORY MANAGEMENT SYSTEM")
    print_line2()

    default_supplier = Supplier("SUP001", "Default Supplier", "supply@example.com")
    inventory = Inventory()
    load_inventory(inventory, default_supplier)
    print("Inventory loaded successfully.\n")
    print_menu()

    option = ""
    while option != "8":
        option = input("\nEnter option: ").strip()

        if option == "1":
            print("Current Inventory")
            print_line1()
            inventory.display_all()
            print_line1()
        elif option == "2":
            add_product_menu(inventory, default_supplier)
        elif option == "3":
            update_stock_menu(inventory)
        elif option == "4":
            search_product_menu(inventory)
        elif option == "5":
            save_inventory(inventory)
            print(f"Inventory saved Successfully to {FILENAME}.")
        elif option == "6":
            path = input(f"CSV file path [{CSV_FILENAME}]: ").strip() or CSV_FILENAME
            load_products(path, inventory, default_supplier)
        elif option == "7":
            create_order_menu(inventory)
        elif option == "8":
            print("Saving Inventory before exit...")
            save_inventory(inventory)
            print("Inventory saved Successfully.\n")
            print("Thank you for using Inventory Management System.\nProgram terminated.")
        else:
            print("Invalid option. Please enter 1-8.")


if __name__ == "__main__":
    main()

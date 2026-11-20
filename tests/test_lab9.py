import io
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from order_line import OrderLine
from product_factory import ProductFactory
from discount_strategy import (
    DiscountStrategy,
    NoDiscount,
    PercentageDiscount,
    BulkDiscount,
    StudentDiscount,
)
from main import get_positive_float, load_products


class TestStrategyPattern(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("SUP001", "Acme Corp", "acme@example.com")
        self.product = ProductFactory.create(
            "physical", "P001", "Desk", 125.0, 10, self.supplier
        )

    def test_order_defaults_to_no_discount(self) -> None:
        order = Order("O001")
        order.add_line(self.product, 2)
        self.assertIsInstance(order.get_discount(), NoDiscount)
        self.assertAlmostEqual(order.calculate_total(), 250.0)

    def test_bulk_then_switch_to_percentage_discount(self) -> None:
        order = Order("O002", BulkDiscount(200, 20))
        order.add_line(self.product, 2)  # subtotal = 250.0
        self.assertAlmostEqual(order.calculate_total(), 230.0)

        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225.0)

    def test_bulk_discount_below_threshold_returns_original_total(self) -> None:
        order = Order("O003", BulkDiscount(300, 20))
        order.add_line(self.product, 2)  # subtotal = 250.0 < 300
        self.assertAlmostEqual(order.calculate_total(), 250.0)

    def test_student_discount(self) -> None:
        order = Order("O004", StudentDiscount())
        order.add_line(self.product, 2)  # subtotal = 250.0
        self.assertAlmostEqual(order.calculate_total(), 237.5)

    def test_new_strategy_without_modifying_order(self) -> None:
        class FlatDiscount(DiscountStrategy):
            def __init__(self, amount: float) -> None:
                self.amount = amount

            def apply(self, total: float) -> float:
                return max(0.0, total - self.amount)

        order = Order("O005", FlatDiscount(50.0))
        order.add_line(self.product, 2)
        self.assertAlmostEqual(order.calculate_total(), 200.0)


class TestProductFactory(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("SUP001", "Acme Corp", "acme@example.com")

    def test_create_physical_product(self) -> None:
        product = ProductFactory.create(
            "physical", "P001", "Desk Lamp", 25.0, 10, self.supplier
        )
        self.assertIsInstance(product, Product)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertEqual(product.get_product_id(), "P001")

    def test_create_digital_product(self) -> None:
        product = ProductFactory.create(
            "digital", "D001", "Photo Editor", 49.90, 100, self.supplier
        )
        self.assertIsInstance(product, Product)
        self.assertIsInstance(product, DigitalProduct)
        self.assertEqual(product.get_name(), "Photo Editor")

    def test_unknown_product_type_raises_value_error(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            ProductFactory.create(
                "service", "S001", "Installation", 30.0, 5, self.supplier
            )
        self.assertIn("Unknown product type", str(ctx.exception))


class TestValidation(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("SUP001", "Acme Corp")
        self.valid_product = ProductFactory.create(
            "physical", "P001", "Lamp", 25.0, 10, self.supplier
        )

    def test_price_must_be_greater_than_zero(self) -> None:
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P002", "Zero", 0.0, 5, self.supplier)
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D002", "Neg", -10.0, 5, self.supplier)

    def test_stock_cannot_be_negative(self) -> None:
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P003", "NegStock", 10.0, -1, self.supplier)
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D003", "NegStock", 10.0, -5, self.supplier)
        with self.assertRaises(ValueError):
            self.valid_product.update_stock(-2)

    def test_order_line_quantity_must_be_greater_than_zero(self) -> None:
        with self.assertRaises(ValueError):
            OrderLine(self.valid_product, 0)
        with self.assertRaises(ValueError):
            OrderLine(self.valid_product, -3)


class TestExceptionHandling(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("SUP001", "Acme Corp")
        self.csv_path = Path(__file__).resolve().parent.parent / "products.csv"

    def test_get_positive_float_retries_until_valid(self) -> None:
        buf = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]), redirect_stdout(buf):
            result = get_positive_float("Price: ")
        output = buf.getvalue()
        self.assertAlmostEqual(result, 12.5)
        self.assertIn("Please enter a valid number", output)
        self.assertIn("Please enter a number greater than zero", output)

    def test_load_products_skips_bad_rows_and_loads_valid_rows(self) -> None:
        inventory = Inventory()
        buf = io.StringIO()
        with redirect_stdout(buf):
            load_products(str(self.csv_path), inventory, self.supplier)
        output = buf.getvalue()
        self.assertEqual(len(inventory.get_all_products()), 3)
        self.assertIsNotNone(inventory.search_product("P001"))
        self.assertIsNotNone(inventory.search_product("D001"))
        self.assertIsNotNone(inventory.search_product("P003"))
        self.assertIsNone(inventory.search_product("S001"))
        self.assertIsNone(inventory.search_product("P002"))
        self.assertIn("3 products loaded.", output)
        self.assertIn("Load attempt finished.", output)

    def test_load_products_handles_missing_file_gracefully(self) -> None:
        inventory = Inventory()
        buf = io.StringIO()
        with redirect_stdout(buf):
            load_products("non_existent_products.csv", inventory, self.supplier)
        output = buf.getvalue()
        self.assertEqual(len(inventory.get_all_products()), 0)
        self.assertIn("Products file not found", output)
        self.assertIn("Load attempt finished.", output)


if __name__ == "__main__":
    unittest.main()

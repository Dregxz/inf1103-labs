from physical_product import PhysicalProduct
from digital_product import DigitalProduct


def _make_physical(product_id, d):
    return PhysicalProduct(product_id, d["Name"], d["Price"], d["Stock"], d["Weight"])


def _make_digital(product_id, d):
    return DigitalProduct(product_id, d["Name"], d["Price"], d["Stock"], d["Download_Size"])


_BUILDERS = {
    "physical": _make_physical,
    "digital": _make_digital,
}


def create_product(product_id, details):
    builder = _BUILDERS[details["Type"]]
    return builder(product_id, details)

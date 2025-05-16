import os

from model.json_parse import parse_products
from model.product_model import ClothingProduct
from model.product_model import ElectronicsProduct
from model.product_model import Product

def test_parse_json():
    current_dir = os.path.dirname(__file__)
    json_path = os.path.join(current_dir, 'test_inputs', 'parse_test.json')
    res = parse_products(json_path)
    expected = [
        Product(name="Яблоко", date="25/04/2025", count=30),
        ClothingProduct(name="Кофта", date="22/04/2025", count=40, size=55, material="Шерсть"),
        ElectronicsProduct(name="Бритва", date="24/04/2025", count=30, warranty_time="24/04/2026", brand="Phillips")
    ]
    assert res == expected

import json
from typing import Union, Any

from pydantic import ValidationError

from .product_model import Product, ClothingProduct, ElectronicsProduct


def parse_products(file_path: str) -> list[Product]:
    products: list[Product] = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data: dict = json.load(f)

            for key, value in json_data.items():
                for product_type in [ElectronicsProduct, ClothingProduct, Product]:
                    try:
                        product = product_type(**value)
                        products.append(product)
                        break
                    except ValidationError as e:
                        last_error = e
                        continue
                else:
                    print(f"Failed to parse item {key}:")
                    print(f"Data: {value}")
                    print(f"Error: {last_error}\n")

    except json.JSONDecodeError as e:
        print(f"Невалидный формат JSON в файле: {file_path}: {str(e)}")
        raise
    except UnicodeDecodeError as e:
        print(f"Проблема с кодировкой в файле: {file_path}: {str(e)}")
        raise
    print(products)
    return products


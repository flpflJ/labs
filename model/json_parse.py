import json

from pydantic import ValidationError

from .logger import logger as logger
from .product_model import ClothingProduct
from .product_model import ElectronicsProduct
from .product_model import Product


def parse_products(file_path: str) -> list[Product]:
    products: list[Product] = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data: list[dict] = json.loads(f.read())
            for item in json_data:
                for product_type in [ElectronicsProduct, ClothingProduct, Product]:
                    try:
                        product = product_type(**item)
                        products.append(product)
                        break
                    except ValidationError as e:
                        last_error = e
                        #logger.critical(f"{e}: something not right.")
                        continue
                else:
                    logger.error(f"{last_error}: something not right.")

    except json.JSONDecodeError as e:
        #print(f"Невалидный формат JSON в файле: {file_path}: {str(e)}")
        logger.critical(f"Невалидный формат JSON в файле: {file_path}: {str(e)}")
        raise
    except UnicodeDecodeError as e:
        #print(f"Проблема с кодировкой в файле: {file_path}: {str(e)}")
        logger.critical(f"Проблема с кодировкой в файле: {file_path}: {str(e)}")
        raise
    print(products)
    return products

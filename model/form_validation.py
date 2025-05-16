from enum import Enum
from typing import Tuple


class Fields(Enum):
    name = 'Название продукта'
    date = 'Дата поступления'
    count = 'Количество продукта'
    warranty_time = 'Дата окончания гарантии'
    brand = 'Название бренда'
    size = 'Размер'
    material = 'Материал'

def validate_data(data: dict) -> Tuple[bool, str]:
    errors = [f"Поле '{key}' не может быть пустым" for key, val in data.items() if not val]
    return not errors, errors[0] if errors else ""

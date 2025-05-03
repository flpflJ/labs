import json
from datetime import datetime

from model.logger import logger


def serializer(obj):
    try:
        if isinstance(obj, datetime):
            return obj.strftime('%d/%m/%Y')
    except Exception as e:
        logger.error(f'Datetime serializer error. Value: {obj}')
        print(e)

def save_to_file(products: list, filename: str):
    with open(filename, 'w') as f:
        f.write(products)

def save_to_json(products: list, filename: str):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump([_.model_dump() for _ in products], f, default=serializer, ensure_ascii=False, indent=4)

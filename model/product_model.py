from datetime import datetime
from typing import Any

from pydantic import BaseModel, field_validator, ValidationError, ConfigDict

class Product(BaseModel):
    name: str
    date: datetime
    count: int

    @field_validator('date', mode='before')
    @classmethod
    def dateCheck(cls, value: Any) -> datetime:
        """Валидатор для преобразования строки в datetime"""
        if isinstance(value, datetime):
            return value

        try:
            return datetime.strptime(value, "%d/%m/%Y")
        except (ValueError, TypeError) as e:
            raise ValueError(
                f"Некорректный формат даты. Ожидается ДД/ММ/ГГГГ. Ошибка: {str(e)}"
            )

    @property
    def creation_date_formatted(self) -> str:
        return self.date.strftime("%d/%m/%Y")

    model_config = ConfigDict(
        json_encoders={datetime: lambda dt: dt.strftime("%d/%m/%Y")},extra="forbid")

class ElectronicsProduct(Product):
    warranty_time: datetime
    brand: str

    @field_validator('warranty_time',mode='before')
    def dateCheck(cls, value: Any) -> datetime:
        return Product.date_check(value)

class ClothingProduct(Product):
    size: int
    material: str

    @field_validator('size')
    @classmethod
    def check_size(cls, value: int):
        if not 40 <= value <= 66:
            raise ValueError("Size must be in range [40, 66]")
        return value
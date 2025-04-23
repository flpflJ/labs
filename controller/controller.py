import traceback
from datetime import datetime
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QInputDialog, QDialog, QMainWindow
from pydantic import ValidationError
from enum import Enum

from model.product_model import Product, ClothingProduct, ElectronicsProduct
from model.json_parse import parse_products
from model.form_validation import validate_data
from view.get_data_dialog import FileAddDialog
from view.main_window import MainWindow
from model.file_save import save_to_json, save_to_file


class ProductManager:
    def __init__(self, view):
        self.view: MainWindow = view
        self.products: list[Product] = []

    def add_manually(self):
        product_types = ["Product", "ClothingProduct", "ElectronicsProduct"]
        product_type, ok = QInputDialog.getItem(self.view, "Выберите тип файла", "Тип файла:", product_types, 0, False)
        if ok and product_type:
            dialog = FileAddDialog(product_type, self.view)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_data()
                is_valid, error_message = validate_data(data)
                if not is_valid:
                    QMessageBox.warning(self.view, "Ошибка валидации", error_message)
                    return

                try:
                    if product_type == "ClothingProduct":
                        self.products.append(ClothingProduct(
                            name=data["name"],
                            date=datetime.strptime(data["date"], "%d/%m/%Y"),
                            count=int(data["count"]),
                            size=int(data["size"]),
                            material=data["material"]
                        ))
                    elif product_type == "ElectronicsProduct":
                        self.products.append(ElectronicsProduct(
                            name=data["name"],
                            date=datetime.strptime(data["date"], "%d/%m/%Y"),
                            count=int(data["count"]),
                            warranty_time=datetime.strptime(data["warranty_time"],"%d/%m/%Y"),
                            brand=data["brand"]
                        ))
                    else:
                        self.products.append(Product(
                            name=data["name"],
                            date=datetime.strptime(data["date"], "%d/%m/%Y"),
                            count=int(data["count"])
                        ))
                    self.view.safe_table_update(self.products)
                except ValidationError as e:
                    QMessageBox.warning(self.view, "Ошибка валидации", str(e))
                except ValueError as e:
                    QMessageBox.warning(self.view, "Ошибка ввода", f"Недопустимый формат: {e}")

    def add_from_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self.view,
            "Открыть JSON файл",
            "",
            "JSON Files (*.json)"
        )

        if not filename:
            return

        try:
            parsed_products = parse_products(filename)

            valid_products = []
            for p in parsed_products:
                if isinstance(p, Product):
                    valid_products.append(p)

            self.products.extend(valid_products)
            self.view.safe_table_update(self.products)

        except Exception as e:
            QMessageBox.critical(
                self.view,
                "Ошибка загрузки",
                f"Невозможно загрузить файл:\n{str(e)}"
            )
            self.view.safe_table_update(self.products)

    def delete_selected(self):
        selected_row = self.view.table.currentRow()
        if selected_row >= 0:
            self.products.pop(selected_row)
            self.view.safe_table_update(self.products)
        else:
            QMessageBox.warning(self.view, "Внимание", "Поле не выбрано")

    def save_to_file(self):
        filename, ok = QInputDialog.getText(self.view, 'Введите имя файла', 'Имя файла:')
        if ok and filename:
            save_to_json(self.products, filename)
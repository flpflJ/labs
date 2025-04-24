from PyQt6.QtWidgets import (
    QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget, QPushButton, QMessageBox, QLabel
)
from PyQt6.QtCore import Qt
from datetime import datetime
from model.product_model import *


class MainWindow(QMainWindow):
    COLUMNS = ["Тип", "Имя", "Дата поступления", "Количество", "Детали"]
    DATE_FORMAT = "%d/%m/%Y"

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.clicked_count = 0
        self.init_ui()
        self.setGeometry(200, 200, 800, 600)

    def init_ui(self):
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.COLUMNS))
        self.table.setHorizontalHeaderLabels(self.COLUMNS)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        buttons = [
            ("Добавить вручную", self.controller.add_manually),
            ("Добавить из файла", self.controller.add_from_file),
            ("Удалить выбранную строку", self.controller.delete_selected),
            ("Сохранить в файл", self.controller.save_to_file)
        ]

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        for text, handler in buttons:
            btn = QPushButton(text)
            btn.clicked.connect(lambda _, h=handler: (self.increment_counter(),h()))
            layout.addWidget(btn)
        self.new_label = QLabel(f"Нажатий на кнопки: {self.clicked_count}")
        layout.addWidget(self.new_label)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def safe_table_update(self, products):
        try:
            self.table.setRowCount(0)
            self.table.setRowCount(len(products))

            for row, product in enumerate(products):
                if not isinstance(product, Product):
                    raise ValueError("Invalid product type")

                self.add_table_row(row, product)

        except Exception as e:
            self.show_error(f"Ошибка обновления таблицы: {str(e)}")
            self.controller.reload_data()

    def add_table_row(self, row, product):
        items = [
            product.__class__.__name__,
            product.name,
            self.format_date(product.date),
            str(product.count),
            self.get_details(product)
        ]

        for col, text in enumerate(items):
            item = QTableWidgetItem(text)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row, col, item)

    def format_date(self, date):
        if isinstance(date, datetime):
            return date.strftime(self.DATE_FORMAT)
        try:
            return datetime.strptime(date, self.DATE_FORMAT).strftime(self.DATE_FORMAT)
        except:
            return "Invalid Date"

    def get_details(self, product):
        if isinstance(product, ElectronicsProduct):
            return f"Бренд: {product.brand} | Гарантия: {self.format_date(product.warranty_time)}"
        if isinstance(product, ClothingProduct):
            return f"Размер: {product.size} | Материал: {product.material}"
        return ""

    def show_error(self, message):
        QMessageBox.critical(self, "Ошибка", message)

    def get_selected_row(self):
        return self.table.currentRow()

    def clear_table(self):
        self.table.setRowCount(0)

    def increment_counter(self):
        self.clicked_count += 1
        self.new_label.setText(f"Нажатий на кнопки: {self.clicked_count}")
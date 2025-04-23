from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox


class FileAddDialog(QDialog):
    def __init__(self, product_type, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Add {product_type}")
        self.product_type = product_type

        self.name_input = QLineEdit()
        self.date_input = QLineEdit()
        self.count_input = QLineEdit()

        self.warranty_time_input = QLineEdit()
        self.brand_input = QLineEdit()

        self.size_input = QLineEdit()
        self.material_input = QLineEdit()

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout = QFormLayout()
        layout.addRow("Name:", self.name_input)
        layout.addRow("Date (DD/MM/YYY):", self.date_input)
        layout.addRow("Count:", self.count_input)

        if product_type == "ElectronicsProduct":
            layout.addRow("Warranty time:", self.warranty_time_input)
            layout.addRow("Brand:", self.brand_input)
        elif product_type == "ClothingProduct":
            layout.addRow("Size(40-66):", self.size_input)
            layout.addRow("Material", self.material_input)

        layout.addWidget(self.button_box)
        self.setLayout(layout)

    def get_data(self):
        data = {
            "name": self.name_input.text(),
            "date": self.date_input.text(),
            "count": self.count_input.text()
        }
        if self.product_type == "ElectronicsProduct":
            data["warranty_time"] = self.warranty_time_input.text()
            data["brand"] = self.brand_input.text()
        elif self.product_type == "ClothingProduct":
            data["size"] = self.size_input.text()
            data["material"] = self.material_input.text()
        return data

    def validate_data(self):
        data = self.get_data()
        for key, value in data.items():
            if not value:
                return False, f"Field '{key}' cannot be empty."
        return True, ""
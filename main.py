import sys

from PyQt6.QtWidgets import QApplication

from controller.controller import ProductManager
from view.main_window import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = ProductManager(None)
    view = MainWindow(controller)
    controller.view = view
    view.show()
    sys.exit(app.exec())

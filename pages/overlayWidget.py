from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt


class OverlayWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: rgba(10, 10, 30, 50); border-radius: 10px;")
        self.setGeometry(100, 100, 500, 500)  # Position and size of the overlay
        self.label = QLabel("This is an overlay!", self)

        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(50, 50, 200, 50)
        self.setVisible(False)

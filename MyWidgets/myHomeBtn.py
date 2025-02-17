from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon

class MyHomeButton(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.home_button = QPushButton("Home")
        self.home_button.setIcon(QIcon("assets/Home.png"))
        self.home_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.home_button.clicked.connect(self.go_home)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.home_button)
        self.setLayout(self.layout)

    def go_home(self):
        # This will trigger a slot to go back to the home screen
        if self.parent():
            self.parent().go_back()  # You should define a go_back method in the parent class

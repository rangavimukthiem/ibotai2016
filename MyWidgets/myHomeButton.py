# myHomebtn--------------------------------
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout



class MyHomeButton(QWidget):
    def __init__(self, parent=None,):
        super().__init__(parent)
        self.parent_window=parent
        self.setStyleSheet("""background-color: #4CAF50;""")
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
        self.parent_window.stack.setCurrentWidget(self.parent_window.HomeScreen)

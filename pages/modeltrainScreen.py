from PyQt5.QtWidgets import QWidget, QPushButton

class ModelTrainScreen(QWidget):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent_window = parent

        # Setup back button
        self.home_btn = QPushButton("Back", self)
        self.home_btn.clicked.connect(self.go_back)

    def go_back(self):
        # Navigate back to the previous screen
        self.parent_window.stack.setCurrentWidget(self.parent_window.HomeScreen)

        # Optionally set the title for the main window
        self.parent_window.setWindowTitle("Train Your New Model Here")

from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QVBoxLayout,QWidget
from pages import InspectionScreen,HomeScreen,ModelTrainScreen
from MyWidgets.myMenu import MymenuBar



class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Main Layout
        self.MainScreen_layout=QVBoxLayout()

        # Create a stacked widget to manage screens
        self.menu_bar=MymenuBar()
        self.stack = QStackedWidget()


        # Instantiate screens
        self.HomeScreen = HomeScreen(self)  # Passing self.stack as parent
        self.InspectionScreen = InspectionScreen(self)
        self.ModelTrainScreen =ModelTrainScreen(self)

        # Add screens to the stack
        self.stack.addWidget(self.HomeScreen)  # Adding the correct instance
        self.stack.addWidget(self.InspectionScreen)
        self.stack.addWidget(self.ModelTrainScreen)
        self.MainScreen_layout.addWidget(self.menu_bar)
        self.MainScreen_layout.addWidget(self.stack)

        central_widget = QWidget()
        central_widget.setLayout(self.MainScreen_layout)
        self.setCentralWidget(central_widget)
        self.stack.setCurrentWidget(self.HomeScreen)

        # Uncomment if you want to set a title and geometry
        self.setWindowTitle("iBot Ai Inspections 2016")
        self.setGeometry(100, 100, 1200, 800)


if __name__ == "__main__":
    app = QApplication([])

    # Apply stylesheet from the external file
    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())
    app.setApplicationName("iBot Ai Inspections 2016")

    # Create the main window and show it
    window = MainWindow()
    window.show()

    app.exec_()

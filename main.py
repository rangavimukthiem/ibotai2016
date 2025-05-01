import os
import sys
import traceback
import logging

from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QVBoxLayout,QWidget

from MyWidgets.cameraView import CameraThread
from pages import InspectionScreen,HomeScreen,ModelTrainScreen,OverlayWidget
from MyWidgets import MyAppException, CustomExceptionLogBox, MymenuBar, CameraView
from pages.myLogging import MyLogging


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        # Main Layout
        self.MainScreen_layout=QVBoxLayout()
        self.trigger_thread=False

        # Create a stacked widget to manage screens
        self.stack = QStackedWidget()

        # Instantiate screens
        self.OverlayWidget=OverlayWidget(self)
        self.HomeScreen = HomeScreen(self)  # Passing self.stack as parent
        self.InspectionScreen = InspectionScreen(self)

        self.Camera = CameraView()
        CameraView._capture_dir="captured"
        CameraView._camIndex=0
        # signal connections

        self.ModelTrainScreen = ModelTrainScreen(self)
        self.menu_bar = MymenuBar(self)
        self.ModelTrainScreen.newModel_trained_Signal.connect(self.InspectionScreen.load_model_list)

        # Add screens to the stack
        self.stack.addWidget(self.HomeScreen)  # Adding the correct instance
        self.stack.addWidget(self.InspectionScreen)
        self.stack.addWidget(self.ModelTrainScreen)
        self.stack.addWidget(self.OverlayWidget)
        self.MainScreen_layout.addWidget(self.menu_bar)
        self.MainScreen_layout.addWidget(self.stack)
        self.MainScreen_layout.addWidget(exception_logger)

        central_widget = QWidget()
        central_widget.setLayout(self.MainScreen_layout)
        self.setCentralWidget(central_widget)
        self.stack.setCurrentWidget(self.HomeScreen)

        # Uncomment if you want to set a title and geometry
        self.setWindowTitle("iBot Ai Inspections 2016")



# Global Exception Handler
def handleCustomExceptions(exception_logger):



    def global_exception_handler(exc_type, exc_value, exc_traceback):
        error_message = "".join(traceback.format_exception(exc_type, exc_value,exc_traceback))
        if exc_type == MyAppException:
            exception_logger.log(f"\u26A0 Custom Exception:\n{error_message}")
            MyLogging.log_error(error_message)

        else:
            exception_logger.log(f"\u274C Uncaught Exception:\n{error_message}")
            MyLogging.log_error(error_message)

    sys.excepthook = global_exception_handler

if __name__ == "__main__":
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    app = QApplication([])
    logger = MyLogging()
    screen_width = app.primaryScreen().size().width()

    exception_logger = CustomExceptionLogBox()
    handleCustomExceptions(exception_logger)
    exception_logger.log(text=f" Hi... \U0001F60E I'm ready...")


    # Apply stylesheet from the external file
    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read()
         )
    app.setApplicationName("iBot Ai Inspections 2016")
    # Create the main window and show it
    window = MainWindow()
    window.show()
    app.exec_()

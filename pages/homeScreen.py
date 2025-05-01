from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from MyWidgets import CameraView, MyAppException


class HomeScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window=parent

        # Optionally set the title for the main window
        self.parent_window.setWindowTitle("iBot Ai Inspections 2016")

        # Home Screen layouts
        self.home_main_layout = QVBoxLayout()
        self.HeaderLayout = QHBoxLayout()
        self.Toolbar_layout=QHBoxLayout()
        self.Body_layout=QHBoxLayout()
        self.Camera_box_layout=QVBoxLayout()
        self.Controllers_layout = QVBoxLayout()
        self.Footer_layout = QHBoxLayout()


        # Layout tree design
        self.home_main_layout.addLayout(self.HeaderLayout)
        self.home_main_layout.addLayout(self.Body_layout)
        self.home_main_layout.addLayout(self.Footer_layout)
        self.Body_layout.addLayout(self.Camera_box_layout)
        self.Body_layout.addLayout(self.Controllers_layout)



        # Widget Arrangement Body layout

        self.camera=CameraView()

        self.Camera_box_layout.addWidget(self.camera)

        self.Controllers_label = QLabel("Controllers")
        self.Controllers_layout.addWidget(self.Controllers_label)

        # Widget Arrangement Footer layout



        # binding Home Main Layout to Self Layout
        self.setLayout(self.home_main_layout)













from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton

class HomeScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window=parent



        # Optionally set the title for the main window
        self.parent_window.setWindowTitle("Train Your New Model Here")

        # Home Screen layout Tree
        home_layout = QVBoxLayout()
        HeaderLayout = QHBoxLayout()




        Toolbar_layout=QHBoxLayout()
        Inspection_btn = QPushButton("Start Inspections ")

        Train_btn = QPushButton("Start Training ")
        Toolbar_layout.addWidget(Train_btn)
        Toolbar_layout.addWidget(Inspection_btn)


        try:
            Inspection_btn.clicked.connect(lambda: self.parent_window.stack.setCurrentWidget(self.parent_window.InspectionScreen))
            Train_btn.clicked.connect(lambda: self.parent_window.stack.setCurrentWidget(self.parent_window.ModelTrainScreen))
        except Exception as e:
            print(f"Page Routing Error >>> {e}")







        Menubar_layout=QHBoxLayout()
        home_btn=QPushButton()
        home_btn.setGeometry(50, 50, 50, 50)

        # Set the home icon

        Menubar_layout.addWidget(home_btn)
        Body_layout=QHBoxLayout()
        Camera_box_layout=QVBoxLayout()
        Camera_box_label = QLabel("RealTime View")
        Camera_box_layout.addWidget(Camera_box_label)
        Controllers_layout=QVBoxLayout()
        Controllers_label = QLabel("Controllers")
        Controllers_layout.addWidget(Controllers_label)
        Footer_layout=QHBoxLayout()
        Footer_label = QLabel("RealTime Log")

        Footer_layout.addWidget(Footer_label)



        # layout Arrangements
        HeaderLayout.addLayout(Menubar_layout)
        HeaderLayout.addLayout(Toolbar_layout)
        Body_layout.addLayout(Camera_box_layout)

        Body_layout.addLayout(Controllers_layout)
        home_layout.addLayout(HeaderLayout)
        home_layout.addLayout(Body_layout)
        home_layout.addLayout(Footer_layout)
        self.setLayout(home_layout)

        self.setWindowTitle("iBot Ai Inspections 2016")








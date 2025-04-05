# myMenuBar----------------------------------
import traceback

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton

from MyWidgets import MyPageNavigationBtn, MyHomeButton


class MymenuBar(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.parent_window=parent
        self.menu_layout=QHBoxLayout()
#       List of Menu Widgets
        try:
            self.menu_layout.addWidget(MyHomeButton(self.parent_window))
            self.inspection_page_btn = MyPageNavigationBtn("Start Inspections",parent=self.parent_window,page=self.parent_window.InspectionScreen)
            self.overlay_btn = MyPageNavigationBtn("Train Inspection Model",parent=self.parent_window,page=self.parent_window.ModelTrainScreen)
            self.train_page_btn = MyPageNavigationBtn("Overlay screen", parent=self.parent_window,page=self.parent_window.OverlayWidget)

        except Exception as e:
            print("Error Type:", type(e).__name__)  # Name of the exception
            print("Error Message:", str(e))  # Exception message
            print("Cause:", e.__cause__)  # Cause of the exception
            print("Context:", e.__context__)  # Context of the exception
            print("Traceback:")
            print("".join(traceback.format_exception(None, e, e.__traceback__)))

        self.menu_layout.addWidget(self.inspection_page_btn)
        self.menu_layout.addWidget(self.train_page_btn)
        self.menu_layout.addWidget(self.overlay_btn)
        self.setLayout(self.menu_layout)





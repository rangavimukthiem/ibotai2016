from PyQt5.QtWidgets import QWidget,QHBoxLayout
from MyWidgets import myHomeBtn


class MymenuBar(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)

        self.parent_window=parent


        menu_layout=QHBoxLayout()


#       List of Menu Widgets
        menu_layout.addWidget(myHomeBtn.MyHomeButton())











        self.setLayout(menu_layout)




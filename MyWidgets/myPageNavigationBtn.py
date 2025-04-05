# myPushBtn ---------------------------------
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton


class MyPageNavigationBtn(QWidget):
    def __init__(self, name="NewPageNavigationButon",parent=None,page:QWidget=None):
        super().__init__(parent)

        self.parent_window=parent
        self.page=page


        menu_layout = QHBoxLayout()
        self.Btn = QPushButton(name)

        menu_layout.addWidget(self.Btn)
        self.setLayout(menu_layout)
        self.Btn.clicked.connect(self.btnFunction)


    def btnFunction(self):
        self.page.setVisible(True)
        self.parent_window.stack.setCurrentWidget(self.page)

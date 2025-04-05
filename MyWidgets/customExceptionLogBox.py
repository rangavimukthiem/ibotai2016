from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit
from PyQt5.QtCore import Qt
import logging


class CustomExceptionLogBox(QWidget):

    _log = None  # Singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._log is None:
            cls._log = super().__new__(cls)
        return cls._log

    def __init__(self):
        super().__init__()

        if hasattr(self, "initialized"):  # Prevent re-initialization
            return

        self.setFixedHeight(230)

        self.log_layout = QVBoxLayout()
        self.log_box_label = QLabel("Realtime Log")
        self.log_layout.addWidget(self.log_box_label)

        self.log_output = QTextEdit()
        self.log_output.setStyleSheet("""QTextEdit {
            background-color: #2C3930;
            color: #06D001;
            border: 1px solid #26355D;
            font-size:18px;
        }""")
        self.log_output.setReadOnly(True)
        self.log_layout.addWidget(self.log_output)

        self.setLayout(self.log_layout)
        self.initialized = True  # Mark as initialized

    def write(self, text: str):
        """Append new text and ensure it auto-scrolls to the bottom."""
        self.log_output.append(text)  # Append new text to the QTextEdit
        self.auto_scroll_to_bottom()

    def auto_scroll_to_bottom(self):
        """Automatically scroll to the bottom of the QTextEdit."""
        scrollbar = self.log_output.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())  # Scroll to the bottom

    @staticmethod
    def log(text: str):
        """Log function to write the log message."""
        if CustomExceptionLogBox._log is not None:
            CustomExceptionLogBox._log.write(text)

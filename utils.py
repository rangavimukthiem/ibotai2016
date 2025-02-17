import os
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QWidget, QTextEdit, QComboBox
)

# return date time stamp ex: 2025-01-29 22-56-44
def get_current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H-%M-%S")




def find_files_by_extension(directory, extensions):
    # List to store files matching the extensions
    matching_files = []

    # Traverse the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if file extension matches any of the known extensions
            if file.lower().endswith(tuple(extensions)):
                matching_files.append(os.path.join(root, file))  # Add the full path of the file

    return matching_files


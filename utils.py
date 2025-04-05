import os
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QWidget, QTextEdit, QComboBox
)

# Timer to update camera feed
import threading

class TimeBomb:
    _timer = None  # Static variable to store the timer instance

    @staticmethod
    def start(countdown, trigger_function):
        """Starts the countdown timer."""
        print(f"💣 Time bomb activated! Exploding in {countdown} seconds...")

        # If there's an existing timer, cancel it before starting a new one
        if TimeBomb._timer:
            TimeBomb._timer.cancel()

        # Create a new timer
        TimeBomb._timer = threading.Timer(countdown, trigger_function)
        TimeBomb._timer.start()

    @staticmethod
    def cancel():
        """Cancels the countdown before detonation."""
        if TimeBomb._timer:
            TimeBomb._timer.cancel()
            print("🛑 Bomb defused!")

    @staticmethod
    def reset(new_countdown, new_trigger_function):
        """Resets the bomb with a new countdown and function."""
        TimeBomb.cancel()  # Stop any existing bomb
        TimeBomb.start(new_countdown, new_trigger_function)








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


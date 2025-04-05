import os

from PyQt5.QtCore import QThread, pyqtSignal
import gc
import time
import numpy as np
import tensorflow as tf
import tensorflow.keras.backend as k
import cv2
import serial
from PyQt5.QtWidgets import QWidget, QCheckBox, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QLabel
from MyWidgets import CustomExceptionLogBox, MyAppException, CameraView
from utils import find_files_by_extension


class ClassifyThread(QThread):
    # Define signals for communication with the main thread
    result_signal = pyqtSignal(int)  # Send prediction class_id back to main thread
    error_signal = pyqtSignal(str)   # Send error message back to main thread

    def __init__(self, model, image, is_continuous_inspection, parent=None):
        super().__init__(parent)
        self.model = model
        self.image = image
        self.is_continuous_inspection = is_continuous_inspection

    def run(self):
        """ This is the method that will run in a separate thread. """
        thread_count = 1
        try:
            while self.is_continuous_inspection:
                time.sleep(0.5)  # Continuous loop

                try:
                    # Preprocess image and make predictions
                    processed_image = self.preprocess_image(self.image)
                    prediction = self.model.predict(processed_image)

                    class_id = np.argmax(prediction)

                    # Emit result back to the main thread
                    self.result_signal.emit(class_id)

                    # Log the results
                    CustomExceptionLogBox.log(f"Prediction result: {class_id} Count: {thread_count}")

                    # Clean up
                    del processed_image, prediction, class_id
                    gc.collect()

                except Exception as e:
                    # Emit error message if processing fails
                    self.error_signal.emit(str(e))

                thread_count += 1

        except Exception as e:
            # Emit error message if there's an issue with the thread
            self.error_signal.emit(f"Error in classification thread: {e}")

    def preprocess_image(self, image):
        """ Preprocess the image before feeding it to the model """
        resized_image = cv2.resize(image, (128, 128))
        processed_image = np.expand_dims(resized_image, axis=0)
        del resized_image
        gc.collect()
        return processed_image


class InspectionScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.is_continuous_inspection_enabled = False
        self.selected_model = None
        self.loaded_model = tf.keras.Model
        self.setWindowTitle("iBot Ai Inspections")
        self.setGeometry(100, 100, 1200, 800)

        # UI elements
        self.checkbox = QCheckBox("Continuous Inspection!", self)
        self.checkbox.stateChanged.connect(self.checkbox_state_changed)

        self.combo_box = QComboBox()
        self.combo_box.mouseDoubleClickEvent()
        self.combo_box.setEditable(False)
        self.combo_box_label = QLabel("Load a Model", self)
        self.model_name = f"{self.combo_box.currentText()}.h5"

        self.capture_btn = QPushButton("Capture Image")
        self.classify_btn = QPushButton("Start")
        self.select_capture_folder_btn = QPushButton("Select Folder For Capture Data")

        # Layouts
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.checkbox)
        button_layout.addWidget(self.combo_box_label)
        button_layout.addWidget(self.combo_box)
        button_layout.addWidget(self.select_capture_folder_btn)
        button_layout.addWidget(self.capture_btn)
        button_layout.addWidget(self.classify_btn)

        self.main_layout = QHBoxLayout()
        self.camera = CameraView()
        self.main_layout.addWidget(self.camera)
        self.main_layout.addLayout(button_layout)

        central_layout = QVBoxLayout()
        central_layout.addLayout(self.main_layout)

        central_widget = QWidget()
        central_widget.setLayout(central_layout)
        self.setLayout(central_layout)

        self.connect_signals()
        self.selected_model = self.combo_box.currentText()
        self.load_model_list()
        self.on_combo_change()

    def connect_signals(self):
        self.capture_btn.clicked.connect(self.capture_image)
        self.select_capture_folder_btn.clicked.connect(self.select_capture_dir)
        self.combo_box.currentTextChanged.connect(self.on_combo_change)
        self.classify_btn.clicked.connect(self.classify_image)

    def checkbox_state_changed(self):
        if self.checkbox.isChecked():
            self.is_continuous_inspection_enabled = True
            CustomExceptionLogBox.log("Continuous inspection is turned on..")

    def load_model_list(self):
        try:
            self.models = find_files_by_extension("models", [".h5", "keras"])
            if len(self.models) == 0:
                CustomExceptionLogBox.log(f"{len(self.models)} No models found. Please train a model and try")

            for model in self.models:
                self.combo_box.addItem(model)

            CustomExceptionLogBox.log(f"{len(self.models)} models found. ")
        except Exception as e:
            raise MyAppException(f"No models to load: {e}")

    def on_combo_change(self):
        self.selected_model = self.combo_box.currentText()

    def capture_image(self):
        self.camera.shoot = True

    def select_capture_dir(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Capture Data Folder")
        if folder:
            CameraView._capture_dir = folder
            CustomExceptionLogBox.log(f"Capture data folder selected: {folder}")

    def load_pretrained_model(self):
        path = self.selected_model
        try:
            CustomExceptionLogBox.log(f"Loading model: {path}")
            if os.path.exists(path):
                self.loaded_model = tf.keras.models.load_model(path, compile=False)
                CustomExceptionLogBox.log(f"Model loaded: {path}")
                return self.loaded_model
        except Exception as e:
            raise MyAppException(f"Model not found at {path}")

    def classify_image(self):
        """ Start classification in a separate thread using QThread """
        self.inspect = True
        # Load the model
        self.load_pretrained_model()

        # Create the thread and connect signals
        self.classify_thread = ClassifyThread(self.loaded_model, self.camera.latest_image, self.is_continuous_inspection_enabled)
        self.classify_thread.result_signal.connect(self.handle_classification_result)
        self.classify_thread.error_signal.connect(self.handle_error)
        self.classify_thread.start()

    def handle_classification_result(self, class_id):
        """ Handle the result from the classification thread """
        CustomExceptionLogBox.log(f"Received classification result: {class_id}")
        print(f"Received classification result: {class_id}")
        self.send_signal_to_hardware(class_id)

    def handle_error(self, error_message):
        """ Handle errors from the classification thread """
        CustomExceptionLogBox.log(f"Error in classification: {error_message}")

    def send_signal_to_hardware(self, class_id):
        try:
            arduino = serial.Serial('COM3', 9600, timeout=1)
            arduino.write(str(class_id).encode())
            arduino.close()
            CustomExceptionLogBox.log(f"Signal sent to hardware: {class_id}")
        except Exception as e:
            CustomExceptionLogBox.log(f"Error communicating with hardware: {e}")

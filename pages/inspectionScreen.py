import os
import sys
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import serial
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QWidget, QTextEdit, QComboBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage
from utils import find_files_by_extension, get_current_datetime

class InspectionScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent

        # Setup UI elements
        self.setup_ui()

        # Initialize camera
        self.cap = cv2.VideoCapture(0)

        # Timer to update camera feed
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        # Variables
        self.models = find_files_by_extension("models", [".h5", "keras"])
        self.model = None
        self.model_name = f"{self.combo_box.currentText()}.h5"
        self.train_dir = "dataset/train"
        self.val_dir = "dataset/validation"
        self.capture_dir = "captured/"
        self.captured_image = None

        # Connect signals to slots
        self.connect_signals()

    def setup_ui(self):
        self.setWindowTitle("iBot Ai Inspections")
        self.setGeometry(100, 100, 1200, 800)

        # Combo Box for Model Selection
        self.combo_box = QComboBox(self)
        self.combo_box.setEditable(False)
        self.combo_box_label = QLabel("Load a Model", self)

        # Camera Label for displaying video feed
        self.camera_label = QLabel(self)
        self.camera_label.setFixedSize(640, 480)
        self.camera_label.setStyleSheet("border: 2px solid black; background-color: #f0f0f0;")

        # Create Buttons
        self.home_btn = QPushButton("Back", self)
        self.upload_train_btn = QPushButton("Upload Train Images")
        self.upload_validation_btn = QPushButton("Upload Validation Images")
        self.train_model_btn = QPushButton("Train Model")
        self.capture_btn = QPushButton("Capture Image")
        self.classify_btn = QPushButton("Classify Image")
        self.select_capture_folder_btn = QPushButton("Select Folder For Capture Data")
        self.start_btn = QPushButton("Start")

        # Logs area
        self.log_output = QTextEdit()
        self.log_output.setStyleSheet("""QTextEdit {
    background-color: #2C3930;
    color: #06D001;
    border: 1px solid #26355D;
}""")
        self.log_output.setReadOnly(True)

        # Layouts
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.home_btn)
        button_layout.addWidget(self.combo_box_label)
        button_layout.addWidget(self.combo_box)
        button_layout.addWidget(self.upload_train_btn)
        button_layout.addWidget(self.upload_validation_btn)
        button_layout.addWidget(self.train_model_btn)
        button_layout.addWidget(self.select_capture_folder_btn)
        button_layout.addWidget(self.capture_btn)
        button_layout.addWidget(self.classify_btn)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.camera_label)
        main_layout.addLayout(button_layout)

        central_layout = QVBoxLayout()
        central_layout.addLayout(main_layout)
        central_layout.addWidget(QLabel("Logs:"))
        central_layout.addWidget(self.log_output)

        central_widget = QWidget()
        central_widget.setLayout(central_layout)
        self.setLayout(central_layout)


        # Apply Styles
        self.apply_styles()

    def connect_signals(self):
        self.home_btn.clicked.connect(self.go_back)
        self.upload_train_btn.clicked.connect(self.upload_train_images)
        self.upload_validation_btn.clicked.connect(self.upload_validation_images)
        self.train_model_btn.clicked.connect(self.train_model)
        self.capture_btn.clicked.connect(self.capture_image)
        self.classify_btn.clicked.connect(self.classify_image)
        self.select_capture_folder_btn.clicked.connect(self.select_capture_dir)
        self.combo_box.currentTextChanged.connect(self.on_combo_change)

    def apply_styles(self):
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 15px 32px;
                font-size: 16px;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

    def go_back(self):
        self.parent_window.stack.setCurrentWidget(self.parent_window.HomeScreen)

    def update_frame(self):
        try:
            ret, frame = self.cap.read()
            if ret:
                flipped_frame = cv2.flip(frame, 1)
                frame_rgb = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2RGB)
                height, width, channel = frame_rgb.shape
                step = channel * width
                q_image = QImage(frame_rgb.data, width, height, step, QImage.Format_RGB888)
                self.camera_label.setPixmap(QPixmap.fromImage(q_image))
        except Exception as e:
            self.log_output.append(f"Error updating camera frame: {e}")

    def load_model_list(self):
        try:
            for model in self.models:
                self.combo_box.addItem(model)
            self.log_output.append(f"{len(self.models)} models found.")
        except Exception as e:
            self.log_output.append(f"Error loading models: {e}")

    def on_combo_change(self):
        try:
            model = self.combo_box.currentText()
            self.model_name = f"{model}.h5"
            self.log_output.append(f"Selected Model: {model}")
        except Exception as e:
            self.log_output.append(f"Error changing model: {e}")

    def load_pretrained_model(self):
        try:
            model_filename = f"models/{self.model_name}"
            if os.path.exists(model_filename):
                self.model = tf.keras.models.load_model(model_filename)
                self.log_output.append(f"Model loaded: {model_filename}")
            else:
                self.log_output.append(f"Model {model_filename} not found.")
        except Exception as e:
            self.log_output.append(f"Error loading model: {e}")

    def upload_train_images(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Train Images Folder")
        if folder:
            self.train_dir = folder
            self.log_output.append(f"Train images folder: {folder}")

    def upload_validation_images(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Validation Images Folder")
        if folder:
            self.val_dir = folder
            self.log_output.append(f"Validation images folder: {folder}")

    def train_model(self):
        if not self.train_dir or not self.val_dir:
            self.log_output.append("Please select both train and validation image folders.")
            return
        try:
            datagen = ImageDataGenerator(rescale=1.0 / 255, validation_split=0.1)
            train_data = datagen.flow_from_directory(self.train_dir, target_size=(128, 128), color_mode='rgb', class_mode='sparse', subset='training')
            val_data = datagen.flow_from_directory(self.val_dir, target_size=(128, 128), color_mode='rgb', class_mode='sparse', subset='validation')

            self.model = Sequential([
                Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
                MaxPooling2D((2, 2)),
                Conv2D(64, (3, 3), activation='relu'),
                MaxPooling2D((2, 2)),
                Flatten(),
                Dense(128, activation='relu'),
                Dense(5, activation='softmax')
            ])
            self.model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
            self.model.fit(train_data, validation_data=val_data, epochs=10)
            self.model.save(f"models/{self.model_name}_classifier.h5")
            self.log_output.append(f"Model trained and saved as {self.model_name}_classifier.h5")
        except Exception as e:
            self.log_output.append(f"Error training model: {e}")

    def capture_image(self):
        try:
            ret, frame = self.cap.read()
            if ret:
                self.captured_image = frame
                date_stamp = get_current_datetime()
                save_path = os.path.join(self.capture_dir, f"captured_{date_stamp}.jpg")
                cv2.imwrite(save_path, frame)
                self.log_output.append(f"Image captured and saved as {save_path}")
            else:
                self.log_output.append("Failed to capture image.")
        except Exception as e:
            self.log_output.append(f"Error capturing image: {e}")

    def classify_image(self):
        try:
            if self.model is None:
                self.log_output.append("No trained model available.")
                return
            if self.captured_image is not None:
                image = self.preprocess_image(self.captured_image)
                prediction = self.model.predict(np.expand_dims(image, axis=0))
                class_id = np.argmax(prediction)
                self.log_output.append(f"Classified as class ID: {class_id}")
                self.send_signal_to_hardware(class_id)
            else:
                self.log_output.append("No image available for classification.")
        except Exception as e:
            self.log_output.append(f"Error classifying image: {e}")

    def preprocess_image(self, image):
        resized_image = cv2.resize(image, (128, 128))
        gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
        return gray_image.reshape(128, 128, 3) / 255.0

    def send_signal_to_hardware(self, class_id):
        try:
            arduino = serial.Serial('COM3', 9600, timeout=1)  # Added timeout for better handling of serial connection
            arduino.write(str(class_id).encode())
            arduino.close()
            self.log_output.append(f"Signal sent to hardware: {class_id}")
        except serial.SerialException as e:
            self.log_output.append(f"Error communicating with hardware: {e}")

    def select_capture_dir(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Capture Data Folder")
        if folder:
            self.capture_dir = folder
            self.log_output.append(f"Capture data folder selected: {folder}")

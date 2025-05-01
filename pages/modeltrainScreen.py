import os
from operator import truediv

import cv2
import tensorflow as tf
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QWidget, QTextEdit, QComboBox
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.python.ops.signal.shape_ops import frame

from MyWidgets import MyAppException, CustomExceptionLogBox

from MyWidgets import CameraView
from utils import find_files_by_extension, get_current_datetime


# from utils import find_files_by_extension, get_current_datetime

class ModelTrainScreen(QWidget):
    newModel_trained_Signal = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent

        # Variables
        self.models = find_files_by_extension("models", [".h5", "keras"])
        self.model = None

        self.train_dir = "dataset/train"
        self.val_dir = "dataset/validation"
        self.capture_dir = "captured/"
        self.captured_image = None

        # Combo Box for Model Selection
        self.new_Model_name_label = QLabel("Create New Model", self)
        self.new_Model_name_label.setFixedHeight(40)
        self.new_Model_name_field = QTextEdit()
        self.new_Model_name_field.setFixedHeight(30)
        self.new_Model_name = f"{self.new_Model_name_field.toPlainText()}.h5"
        # Connect signals to slots

        self.setWindowTitle("Train your iBot ")
        self.setGeometry(100, 100, 1200, 800)

        # Create Buttons
        self.train_model_btn = QPushButton("Train Model")
        self.train_model_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #3AAF50;
                        border: 4px;
                        color: white;
                        padding: 15px 32px;
                        font-size: 16px;
                        cursor: pointer;
                    }
                    QPushButton:hover {
                        background-color: #42A049;
                    }
                """)

        self.upload_validation_btn = QPushButton("Upload Validation Images")
        self.upload_train_btn = QPushButton("upload Training images")
        self.capture_btn = QPushButton("Capture Image")

        self.select_capture_folder_btn = QPushButton("Select Folder For Capture Data")
        self.start_btn = QPushButton("Start")

        # Layouts
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.train_model_btn)

        button_layout.addWidget(self.new_Model_name_label)
        button_layout.addWidget(self.new_Model_name_field)
        button_layout.addWidget(self.upload_train_btn)
        button_layout.addWidget(self.upload_validation_btn)
        button_layout.addWidget(self.select_capture_folder_btn)
        button_layout.addWidget(self.capture_btn)

        self.main_layout = QHBoxLayout()
        self.camera = CameraView()
        self.main_layout.addWidget(self.camera)

        self.main_layout.addLayout(button_layout)
        #
        self.central_layout = QVBoxLayout()
        self.central_layout.addLayout(self.main_layout)

        central_widget = QWidget()
        central_widget.setLayout(self.central_layout)
        self.setLayout(self.central_layout)
        self.connect_signals()

    def update_model_name(self):
        self.new_Model_name = self.new_Model_name_field.toPlainText()

    def connect_signals(self):
        self.upload_train_btn.clicked.connect(self.upload_train_images)
        self.upload_validation_btn.clicked.connect(self.upload_validation_images)
        self.train_model_btn.clicked.connect(self.train_model)
        self.select_capture_folder_btn.clicked.connect(self.select_capture_dir)
        self.capture_btn.clicked.connect(self.capture_image)
        self.new_Model_name_field.textChanged.connect(self.update_model_name)

    def capture_image(self):
        try:

            self.camera.shoot = True
        except Exception as e:
            raise MyAppException(e)

    def upload_train_images(self):
        folder = QFileDialog.getExistingDirectory(self, "Select a Folder for Training Images ")
        if folder:
            self.train_dir = folder
            CustomExceptionLogBox.log(text=f"Train images folder: {folder}")

    def upload_validation_images(self):
        folder = QFileDialog.getExistingDirectory(self, "Select a Folder for Validation Images ")
        if folder:
            self.val_dir = folder
            raise MyAppException(f"Validation images folder: {folder}")

    def train_model(self):
        if not self.train_dir or not self.val_dir or not self.new_Model_name:
            raise MyAppException(
                "Please select both train and validation image folders and new model name then re try.")

        try:
            train_datagen = ImageDataGenerator(rescale=1.0 / 255,
                                         rotation_range=15,
                                         zoom_range=0.1,
                                         width_shift_range=0.1,
                                         height_shift_range=0.1,
                                         shear_range=0.1,
                                         horizontal_flip=True,
                                         fill_mode='nearest')

            train_data = train_datagen.flow_from_directory(
                self.train_dir,
                target_size=(128, 128),
                color_mode='rgb',
                class_mode='sparse',
                batch_size=32,
                seed=123,
                shuffle=True
            )
            validation_datagen = ImageDataGenerator(rescale=1.0 / 255)

            val_data = validation_datagen.flow_from_directory(
                self.val_dir,
                target_size=(128, 128),
                color_mode='rgb',
                class_mode='sparse',
                batch_size=32

            )

            model = Sequential([
                Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
                MaxPooling2D((2, 2)),
                Conv2D(64, (3, 3), activation='relu'),
                MaxPooling2D((2, 2)),
                Flatten(),
                Dense(128, activation='relu'),
                Dense(5, activation='softmax')
            ])
            # Debugging: Print dataset size
            CustomExceptionLogBox.log(text=f"Training started ....")
            CustomExceptionLogBox.log(text=f"Train dataset size: {len(train_data)}")
            CustomExceptionLogBox.log(text=f"Validation dataset size: {len(val_data)}")

            model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

            model.fit(train_data, validation_data=val_data, epochs=10)

            model.save(f"models/{self.new_Model_name}_classifier.h5")

            CustomExceptionLogBox.log(text=f"Model trained and saved as {self.new_Model_name}_classifier.h5")
            self.newModel_trained_Signal.emit(True)


        except Exception as e:
            raise MyAppException(f"Error training model: {e}")

    def select_capture_dir(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Capture Data Folder")
        if folder:
            CameraView._capture_dir = folder
            CustomExceptionLogBox.log(text=f"Capture data folder selected: {folder}")

import gc

from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QFileDialog, \
    QRadioButton, QSlider
from PyQt5.QtCore import QTimer, Qt
from MyWidgets import CameraView
from MyWidgets import CustomExceptionLogBox, MyAppException
from utils import find_files_by_extension
from pages import ClassifyThread
from pages import Hardware_interface

import tensorflow as tf
import os

class InspectionScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.loaded_model = None
        self.stop_signal = False
        self.selected_model=None
        self.classify_thread=None
        self.stop_run =False
        self.InspectionRate=200

        self.setWindowTitle("iBot Ai Inspections")
        self.setGeometry(100, 100, 1200, 800)

        # UI
        self.camera = CameraView()
        self.combo_box = QComboBox()
        self.capture_btn = QPushButton("Capture")
        self.classify_btn = QPushButton("Start")
        self.stop_btn = QPushButton("Stop")
        self.select_capture_folder_btn = QPushButton("Select Folder")

        self.radio1 = QRadioButton("Continuous")
        self.radio2 = QRadioButton("Single")
        self.radio3 = QRadioButton("Off")
        self.slider_layout=QHBoxLayout()
        self.slider_lable=QLabel()
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(200)
        self.slider.setMaximum(5000)
        self.slider.setTickInterval(500)
        self.slider.tickInterval(500)

        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setSingleStep(500)  # Arrow keys / Page keys step
        self.slider.setPageStep(500)
        self.slider_layout.addWidget(self.slider_lable)
        self.slider_layout.addWidget(self.slider)

        self.slider.valueChanged.connect(self.slider_value_changed)

        self.thread_timer = QTimer()
        self.thread_timer.timeout.connect(self.operation)

        self._init_layout()
        self._connect_signals()
        self.load_model_list()

    def _init_layout(self):
        layout = QVBoxLayout()
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.radio1)
        radio_layout.addWidget(self.radio2)
        radio_layout.addWidget(self.radio3)

        layout.addLayout(radio_layout)
        layout.addWidget(QLabel("Load Model:"))
        layout.addLayout(self.slider_layout)
        layout.addWidget(self.combo_box)
        layout.addWidget(self.select_capture_folder_btn)
        layout.addWidget(self.capture_btn)
        layout.addWidget(self.classify_btn)
        layout.addWidget(self.stop_btn)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.camera)
        main_layout.addLayout(layout)

        self.setLayout(main_layout)

    def _connect_signals(self):
        self.capture_btn.clicked.connect(lambda: setattr(self.camera, 'shoot', True))

        self.select_capture_folder_btn.clicked.connect(self.select_capture_dir)
        self.classify_btn.clicked.connect(self.classify_image)
        self.stop_btn.clicked.connect(lambda: setattr(self, 'stop_signal', True))
        self.combo_box.currentTextChanged.connect(self.on_combo_change)
        self.stop_btn.clicked.connect(self.stopOperation)

    def slider_value_changed(self):
        self.slider_lable.setText(f"Inspection Rate : {self.slider.value().__int__()}")
        self.InspectionRate=self.slider.value()
        print(f"rate : {self.InspectionRate}")

    def on_combo_change(self):
        self.selected_model = self.combo_box.currentText()
        CustomExceptionLogBox.log(text=f"Selected Model Changed to : {self.selected_model}")

    def load_model_list(self):
        models = find_files_by_extension("models", [".h5"])
        for model in models:
            self.combo_box.addItem(model)

    def select_capture_dir(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            CameraView._capture_dir = folder
            CustomExceptionLogBox.log(f"Capture folder set: {folder}")

    def load_pretrained_model(self):
        path = self.selected_model
        try:
            CustomExceptionLogBox.log(f"Loading model: {path}")
            if os.path.exists(path):
                loaded_model = tf.keras.models.load_model(path, compile=False)
                CustomExceptionLogBox.log(f"Model loaded: {path}")
                print(f"Model loaded: {path}")
                return loaded_model
        except Exception as e:
            raise MyAppException(f"Model not found at {path}")

    def classify_image(self):

        try:
            self.loaded_model = self.load_pretrained_model()
            print("model loaded")
        except MyAppException as e:
            CustomExceptionLogBox.log(str(e))
            print(e)
            return

        if self.radio1.isChecked():
            self.thread_timer.start(self.InspectionRate)
        elif self.radio2.isChecked():
            self.operation()

    def operation(self):
        image = self.camera.latest_image
        if image is None or self.loaded_model is None:
            print("image or model is none")
            return

        classify_thread = ClassifyThread(model=self.loaded_model, image=image)
        classify_thread.result_signal.connect(self.handle_result)
        classify_thread.error_signal.connect(self.handle_error)
        classify_thread.start()
        self.classify_thread = classify_thread
        if self.stop_run:
            classify_thread.stop()

        del classify_thread
        gc.collect()

    def stopOperation(self):
        self.stop_run=True
        self.thread_timer.stop()
        CustomExceptionLogBox.log(text="Operation Stopped by User")


    def handle_result(self, class_id):
        CustomExceptionLogBox.log(f"Prediction: {class_id}")
        # Hardware_interface.send_signal_to_hardware(class_id)

    def handle_error(self, error_msg):
        CustomExceptionLogBox.log(error_msg)

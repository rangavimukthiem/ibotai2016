import gc
import os

from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap
import cv2
import numpy as np

from MyWidgets import CustomExceptionLogBox, MyAppException
from utils import get_current_datetime


class CameraView(QWidget):
    _camera_instance=None
    frame_feed = pyqtSignal(np.ndarray)
    _capture_dir = "captured"
    _cap=None
    _camIndex=0

    def __init__(self):
        super().__init__()
        self.setFixedSize(650, 550)
        self.shoot=False
        self.latest_image=None

        # Ensure a shared camera instance
        if CameraView._camera_instance is None:
            CameraView._camera_instance = self
            print(f"camera index {CameraView._camIndex}")
            print(f"capture folder {CameraView._capture_dir}")
            CameraView._cap = cv2.VideoCapture(CameraView._camIndex)

            if not CameraView._cap.isOpened():
                # raise MyAppException("Failed to open camera device.")
                print("Failed to open camera device.")



        # Initialize the CameraThread and connect the signal
        self.camera_thread = CameraThread(cam_index=CameraView._camIndex)
        self.camera_thread.frame_ready.connect(self.update_pixmap)

        # Camera Label
        self.camera_label = QLabel(self)
        self.camera_label.setStyleSheet("border: 2px solid blue; background-color: #6d706f;")
        self.camera_label.setScaledContents(True)

        layout = QVBoxLayout()
        self.Camera_box_label = QLabel("RealTime View")
        layout.addWidget(self.Camera_box_label)
        layout.addWidget(self.camera_label)
        self.setLayout(layout)

        try:
            # Start the camera thread using QThread
            self.camera_thread.start()
        except Exception as e:
            print(f"Start camera thread error: {e}")

    def update_pixmap(self, frame_rgb):
        # print(f"update pixmap signal recieved...{id(frame_rgb)}")

        if self.shoot:
            self.capture_image(frame_rgb)
        try:
            self.latest_image = frame_rgb.copy()
            # print(f"type of frame feed {type(frame_rgb)}")


            height, width, channel = frame_rgb.shape
            image = QImage(frame_rgb.data, width, height, width * channel, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            self.camera_label.setPixmap(
                pixmap.scaled(self.camera_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.shoot=False
            self.frame_feed.emit(frame_rgb)
        except Exception as e:
            print(f"Updating pixmap error: {e}")

    def closeEvent(self, event):
        """Ensure the camera thread stops when closing the app"""
        self.camera_thread.stop()
        event.accept()

    def capture_image(self,image):


        try:
            date_stamp = get_current_datetime()
            save_path = os.path.join(CameraView._capture_dir, f"captured_{date_stamp}.jpg")
            os.makedirs(CameraView._capture_dir, exist_ok=True)
            rgb_image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            cv2.imwrite(save_path, rgb_image)

            print(f"Image saved to {save_path}")
            CustomExceptionLogBox.log(f"Image captured and saved as {save_path}")
        except Exception as e:
            CustomExceptionLogBox().log(f"Logging: {e}")


class CameraThread(QThread):
    frame_ready = pyqtSignal(np.ndarray)

    def __init__(self, cam_index=0):
        super().__init__()
        self.cap = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)

        if not self.cap.isOpened():
            print("Camera failed to open")
        else:
            print(f"Camera opened successfully on index {cam_index}")
        self.running = True
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)

    def run(self):
        while self.running:
            if not self.cap or not self.cap.isOpened():
                print("Camera is not open")
                return

            try:
                ret, frame = self.cap.read()
                if ret:
                    flipped_frame = cv2.flip(frame, 1)  # Flip horizontally
                    frame_rgb = cv2.cvtColor(flipped_frame,cv2.COLOR_BGR2RGB)
                    self.frame_ready.emit(frame_rgb)
            except Exception as e:
                print(f"Camera running failed: {e}")

    def stop(self):
        self.running = False
        self.quit()
        self.wait()
        if self.cap.isOpened():
            self.cap.release()

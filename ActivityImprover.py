from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QMessageBox,
    QComboBox,
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QIcon
import pyautogui
import sys
import json
import os


# Configuration file path
CONFIG_FILE = "config.json"


class WorkerThread(QThread):
    def __init__(self, interval, distance, parent=None):
        super().__init__(parent)
        self.interval = interval
        self.distance = distance
        self.running = True

    def run(self):
        while self.running:
            current_position = pyautogui.position()
            pyautogui.moveTo(current_position.x + self.distance, current_position.y)
            pyautogui.moveTo(current_position.x, current_position.y)
            QThread.msleep(self.interval)

    def stop(self):
        self.running = False


class ActivityImproverApp(QWidget):
    def __init__(self, user_name):
        super().__init__()
        self.init_ui()
        self.setWindowFlags(
            Qt.WindowCloseButtonHint | Qt.WindowTitleHint | Qt.WindowMinimizeButtonHint
        )
        self.thread = None
        self.load_settings()
        self.username = user_name

    def init_ui(self):
        self.setWindowTitle("Activity Improver")
        self.setGeometry(100, 100, 400, 350)
        self.setStyleSheet(
            "background-color: #eaeaea; font-family: Helvetica, sans-serif; font-size: 16px; color: #333;"
        )

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        self.label = QLabel(f"Welcome to Activity Improver {self.username}", self)
        self.setWindowIcon(QIcon("handshake.ico"))
        self.label.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: #333; font-family: Helvetica, sans-serif;"
        )
        self.layout.addWidget(self.label)

        self.description = QLabel(
            "This app will help you improve your activity by simulating mouse movement at a regular interval.",
            self,
        )
        self.description.setStyleSheet(
            "font-family: Helvetica, sans-serif; font-size: 18px; color: #666;"
        )
        self.layout.addWidget(self.description)

        self.preset_label = QLabel("Select a preset configuration", self)
        self.preset_label.setStyleSheet(
            "font-family: Helvetica, sans-serif; font-size: 18px; color: #666;"
        )
        self.layout.addWidget(self.preset_label)

        self.preset_combo = QComboBox(self)
        self.preset_combo.addItems(["None", "Short Breaks", "Long Breaks"])
        self.preset_combo.setStyleSheet(
            "font-size: 16px; padding: 10px; border-radius: 8px; border: 1px solid #aaa; background-color: #fff;"
        )
        self.preset_combo.currentIndexChanged.connect(self.apply_preset)
        self.layout.addWidget(self.preset_combo)

        self.interval_label = QLabel("Select the interval level in milliseconds", self)
        self.interval_label.setStyleSheet(
            "font-family: Helvetica, sans-serif; font-size: 18px; color: #666;"
        )
        self.layout.addWidget(self.interval_label)

        self.interval_input = QLineEdit(self)
        self.interval_input.setText("100")
        self.interval_input.setPlaceholderText("Enter interval level (e.g., 100)")
        self.interval_input.setStyleSheet(
            "font-size: 16px; padding: 10px; border-radius: 8px; border: 1px solid #aaa; background-color: #fff;"
        )
        self.layout.addWidget(self.interval_input)

        self.distance_label = QLabel("Select the distance level in pixels", self)
        self.distance_label.setStyleSheet(
            "font-family: Helvetica, sans-serif; font-size: 18px; color: #666;"
        )
        self.layout.addWidget(self.distance_label)

        self.distance_input = QLineEdit(self)
        self.distance_input.setText("0.5")
        self.distance_input.setPlaceholderText("Enter distance level (e.g., 0.5)")
        self.distance_input.setStyleSheet(
            "font-size: 16px; padding: 10px; border-radius: 8px; border: 1px solid #aaa; background-color: #fff;"
        )
        self.layout.addWidget(self.distance_input)

        self.start_button = QPushButton("Start", self)
        self.start_button.setStyleSheet(
            "background-color: #4caf50; color: white; padding: 10px; border-radius: 8px; font-size: 16px; font-weight: bold;"
        )
        self.start_button.setFixedHeight(40)
        self.start_button.setCursor(Qt.PointingHandCursor)
        self.start_button.clicked.connect(self.start_thread)
        self.layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.setStyleSheet(
            "background-color: #f44336; color: white; padding: 10px; border-radius: 8px; font-size: 16px; font-weight: bold;"
        )
        self.stop_button.setFixedHeight(40)
        self.stop_button.setCursor(Qt.PointingHandCursor)
        self.stop_button.clicked.connect(self.stop_thread)
        self.layout.addWidget(self.stop_button)

        self.setLayout(self.layout)

    def load_settings(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as file:
                config = json.load(file)
                self.interval_input.setText(str(config.get("interval", 100)))
                self.distance_input.setText(str(config.get("distance", 0.5)))
                self.preset_combo.setCurrentText(config.get("preset", "None"))

    def save_settings(self):
        config = {
            "interval": int(self.interval_input.text()),
            "distance": float(self.distance_input.text()),
            "preset": self.preset_combo.currentText(),
        }
        with open(CONFIG_FILE, "w") as file:
            json.dump(config, file)

    def apply_preset(self):
        preset = self.preset_combo.currentText()
        if preset == "Short Breaks":
            self.interval_input.setText("200")
            self.distance_input.setText("5")
        elif preset == "Long Breaks":
            self.interval_input.setText("1000")
            self.distance_input.setText("10")
        else:
            self.interval_input.setText("100")
            self.distance_input.setText("0.5")

    def start_thread(self):
        interval_str = self.interval_input.text()
        distance_str = self.distance_input.text()

        if not interval_str or not distance_str:
            QMessageBox.critical(
                self,
                "Error",
                "Please set both the interval level and the distance level",
            )
            return

        try:
            interval = int(interval_str)
            distance = float(distance_str)
            if interval <= 0:
                raise ValueError("Interval must be a positive integer")
            if distance < 0:
                raise ValueError("Distance must be a non-negative number")
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Invalid input: {e}")
            return

        if self.thread and self.thread.isRunning():
            QMessageBox.warning(
                self, "Warning", "The activity improver is already running."
            )
            return

        self.thread = WorkerThread(interval, distance)
        self.thread.start()
        self.start_button.setText("Running")
        self.start_button.setStyleSheet(
            "background-color: grey; color: white; border-radius: 5px; padding: 5px 10px; font-size: 16px; font-weight: bold;"
        )
        QMessageBox.information(self, "Started", "The activity improver has started.")

    def stop_thread(self):
        if self.thread and self.thread.isRunning():
            self.thread.stop()
            self.thread.wait()
            self.start_button.setText("Start")
            self.start_button.setStyleSheet(
                "background-color: #4caf50; color: white; border-radius: 5px; padding: 5px 10px; font-size: 16px; font-weight: bold;"
            )
            QMessageBox.information(
                self, "Stopped", "The activity improver has stopped."
            )
        else:
            QMessageBox.information(
                self, "Stopped", "The activity improver is not running."
            )

    def closeEvent(self, event):
        self.save_settings()
        event.accept()

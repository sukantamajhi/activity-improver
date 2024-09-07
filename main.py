from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QMessageBox,
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QIcon
import pyautogui
import sys


class WorkerThread(QThread):
    def __init__(self, interval, parent=None):
        super().__init__(parent)
        self.interval = interval
        self.running = True

    def run(self):
        while self.running:
            # Move mouse cursor slightly
            current_position = pyautogui.position()
            pyautogui.moveTo(current_position.x + 0.5, current_position.y)
            pyautogui.moveTo(current_position.x, current_position.y)
            QThread.msleep(self.interval)

    def stop(self):
        self.running = False


class ActivityImproverApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowFlags(
            Qt.WindowCloseButtonHint | Qt.WindowTitleHint | Qt.WindowMinimizeButtonHint
        )
        self.thread = None

    def init_ui(self):
        self.setWindowTitle("Activity Improver")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background-color: #eaeaea; font-family: Arial, sans-serif;")

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        self.label = QLabel("Welcome to Activity Improver", self)
        # set window icon
        self.setWindowIcon(QIcon("handshake.ico"))
        self.label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        self.layout.addWidget(self.label)

        self.description = QLabel(
            "This app will help you improve your activity by simulating mouse movement at a regular interval.",
            self,
        )
        self.description.setStyleSheet("font-size: 18px; color: #666;")
        self.layout.addWidget(self.description)

        self.interval_label = QLabel("Select the interval level in milliseconds", self)
        self.interval_label.setStyleSheet("font-size: 18px; color: #666;")
        self.layout.addWidget(self.interval_label)

        self.interval_input = QLineEdit(self)
        self.interval_input.setPlaceholderText("Enter interval level (e.g., 1000)")
        self.interval_input.setStyleSheet(
            "font-size: 16px; padding: 10px; border-radius: 8px; border: 1px solid #aaa; background-color: #fff;"
        )
        self.layout.addWidget(self.interval_input)

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

    def start_thread(self):
        interval_str = self.interval_input.text()
        if not interval_str:
            QMessageBox.critical(self, "Error", "Please set the interval level")
            return

        try:
            interval = int(interval_str)
        except ValueError:
            QMessageBox.critical(self, "Error", "Interval must be a number")
            return

        if self.thread and self.thread.isRunning():
            QMessageBox.warning(
                self, "Warning", "The activity improver is already running."
            )
            return

        self.thread = WorkerThread(interval)
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
                "background-color: green; color: white; border-radius: 5px; padding: 5px 10px; font-size: 16px; font-weight: bold;"
            )
            QMessageBox.information(
                self, "Stopped", "The activity improver has stopped."
            )
        else:
            QMessageBox.information(
                self, "Stopped", "The activity improver is not running."
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ActivityImproverApp()
    window.show()
    sys.exit(app.exec_())

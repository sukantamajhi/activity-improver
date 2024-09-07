from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QMessageBox,
)
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
import pyautogui
import sys


class WorkerThread(QThread):
    update_signal = pyqtSignal(str)  # Signal to update status

    def __init__(self, interval, parent=None):
        super().__init__(parent)
        self.interval = interval
        self.running = True

    def run(self):
        while self.running:
            pyautogui.press("control")
            QThread.msleep(self.interval)

    def stop(self):
        self.running = False


class ActivityImproverApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.thread = None

    def init_ui(self):
        self.setWindowTitle("Activity Improver")
        self.setGeometry(100, 100, 350, 250)
        self.setStyleSheet("background-color: #f0f0f0;")

        self.layout = QVBoxLayout()

        self.label = QLabel("Welcome to Activity Improver", self)
        self.label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.layout.addWidget(self.label)

        self.interval_label = QLabel("Select the interval level in milliseconds", self)
        self.interval_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(self.interval_label)

        self.interval_input = QLineEdit(self, placeholderText="Enter interval level")
        self.interval_input.setStyleSheet(
            "font-size: 16px; padding: 5px; border-radius: 5px; border: 1px solid #ccc;"
        )
        self.layout.addWidget(self.interval_input)

        self.start_button = QPushButton("Start", self)
        self.start_button.setStyleSheet(
            "background-color: green; color: white; margin-top: 10px; border-radius: 5px; padding: 5px 10px; font-size: 16px; font-weight: bold;"
        )
        self.start_button.clicked.connect(self.start_thread)
        self.layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.setStyleSheet(
            "background-color: red; color: white; border-radius: 5px; padding: 5px 10px; font-size: 16px; font-weight: bold;"
        )
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

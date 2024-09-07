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
    def __init__(self, interval, distance, parent=None):
        super().__init__(parent)
        self.interval = interval
        self.distance = distance
        self.running = True

    def run(self):
        while self.running:
            # Move mouse cursor slightly
            current_position = pyautogui.position()
            pyautogui.moveTo(current_position.x + self.distance, current_position.y)
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
        # Window settings
        self.setWindowTitle("Activity Improver")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background-color: #eaeaea; font-family: Arial, sans-serif;")

        # Layout settings
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        # Window title
        self.label = QLabel("Welcome to Activity Improver", self)
        # set window icon
        self.setWindowIcon(QIcon("handshake.ico"))
        self.label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        self.layout.addWidget(self.label)

        # Description
        self.description = QLabel(
            "This app will help you improve your activity by simulating mouse movement at a regular interval.",
            self,
        )
        self.description.setStyleSheet("font-size: 18px; color: #666;")
        self.layout.addWidget(self.description)

        # Interval settings
        self.interval_label = QLabel("Select the interval level in milliseconds", self)
        self.interval_label.setStyleSheet("font-size: 18px; color: #666;")
        self.layout.addWidget(self.interval_label)

        # Interval input
        self.interval_input = QLineEdit(self)
        self.interval_input.setText("100")
        self.interval_input.setPlaceholderText("Enter interval level (e.g., 100)")
        self.interval_input.setStyleSheet(
            "font-size: 16px; padding: 10px; border-radius: 8px; border: 1px solid #aaa; background-color: #fff;"
        )
        self.layout.addWidget(self.interval_input)

        # Distance settings
        self.distance_label = QLabel("Select the distance level in pixels", self)
        self.distance_label.setStyleSheet("font-size: 18px; color: #666;")
        self.layout.addWidget(self.distance_label)

        # Distance input
        self.distance_input = QLineEdit(self)
        self.distance_input.setText("0.5")
        self.distance_input.setPlaceholderText("Enter distance level (e.g., 100)")
        self.distance_input.setStyleSheet(
            "font-size: 16px; padding: 10px; border-radius: 8px; border: 1px solid #aaa; background-color: #fff;"
        )
        self.layout.addWidget(self.distance_input)

        # Start button
        self.start_button = QPushButton("Start", self)
        self.start_button.setStyleSheet(
            "background-color: #4caf50; color: white; padding: 10px; border-radius: 8px; font-size: 16px; font-weight: bold;"
        )
        self.start_button.setFixedHeight(40)
        self.start_button.setCursor(Qt.PointingHandCursor)
        self.start_button.clicked.connect(self.start_thread)
        self.layout.addWidget(self.start_button)

        # Stop button
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
        # Get interval and distance values from input fields
        interval_str = self.interval_input.text()
        distance_str = self.distance_input.text()

        # Check if interval and distance are set
        if not interval_str:
            QMessageBox.critical(self, "Error", "Please set the interval level")
            return

        if not distance_str:
            QMessageBox.critical(self, "Error", "Please set the distance level")
            return

        # Convert interval and distance to integers
        try:
            interval = int(interval_str)
            distance = float(distance_str)
        except ValueError:
            QMessageBox.critical(self, "Error", "Interval and distance must be numbers")
            return

        # Check if the thread is already running
        if self.thread and self.thread.isRunning():
            QMessageBox.warning(
                self, "Warning", "The activity improver is already running."
            )
            return

        # Create and start the thread
        self.thread = WorkerThread(interval, distance)
        self.thread.start()
        self.start_button.setText("Running")
        self.start_button.setStyleSheet(
            "background-color: grey; color: white; border-radius: 5px; padding: 5px 10px; font-size: 16px; font-weight: bold;"
        )
        QMessageBox.information(self, "Started", "The activity improver has started.")

    def stop_thread(self):
        # Check if the thread is running
        if self.thread and self.thread.isRunning():
            # Stop the thread
            self.thread.stop()
            # Wait for the thread to finish
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


# Run the app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ActivityImproverApp()
    window.show()
    sys.exit(app.exec_())

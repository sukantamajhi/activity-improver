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
import time
import requests as r

from ActivityImprover import ActivityImproverApp

# Configuration file path
CONFIG_FILE = "config.json"


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 200)
        self.setStyleSheet(
            "background-color: #eaeaea; font-family: Helvetica, sans-serif; font-size: 16px; color: #333;"
        )

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        self.label = QLabel("Enter your email", self)
        self.label.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: #333; font-family: Helvetica, sans-serif;"
        )
        self.layout.addWidget(self.label)

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Enter your email")
        self.email_input.setStyleSheet(
            "font-size: 16px; padding: 10px; border-radius: 8px; border: 1px solid #aaa; background-color: #fff;"
        )
        self.layout.addWidget(self.email_input)

        self.label = QLabel("Enter your password", self)
        self.label.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: #333; font-family: Helvetica, sans-serif;"
        )
        self.layout.addWidget(self.label)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(
            "font-size: 16px; padding: 10px; border-radius: 8px; border: 1px solid #aaa; background-color: #fff;"
        )
        self.layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login", self)
        self.login_button.setStyleSheet(
            "background-color: #4caf50; color: white; padding: 10px; border-radius: 8px; font-size: 16px; font-weight: bold;"
        )
        self.login_button.setFixedHeight(40)
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.clicked.connect(self.login)
        self.layout.addWidget(self.login_button)

        self.setLayout(self.layout)

    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        if not email or not password:
            QMessageBox.critical(self, "Error", "Please enter your email and password")
            return

        print({"email": email, "password": password}, "login data")

        # TODO: Need to change this to the actual API endpoint. Currently we are using a local server of ecom-be.
        response = r.post(
            "http://localhost:4000/api/auth/signin",
            json={"email": email, "password": password},
            headers={"Content-Type": "application/json"},
        )
        print(response.json(), "response")
        if response.status_code == 200:
            user_name = response.json().get("username")
            print(user_name, "user_name")
            self.main_window = ActivityImproverApp(user_name=user_name)

            self.main_window.show()
            self.close()
        else:
            QMessageBox.critical(self, "Error", "Incorrect password")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())

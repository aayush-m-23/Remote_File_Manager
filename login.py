from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QFrame, QMessageBox, QMainWindow, QDialog
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import sys
from register import RegistrationPage
import json
import socket
from tkinter import *
from tkinter import ttk, messagebox
from client import*
from client import RemoteFileManager

SERVER_HOST = '192.168.1.36'
SERVER_PORT = 5050
BUFFER_SIZE = 65536

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(400, 450)

        self.login_frame = QFrame(self)
        self.login_frame.setGeometry(0, 0, 400, 450)
        self.login_frame.setStyleSheet("background-color: #222; border-radius: 10px;")

        self.setup_form()

     def setup_form(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        title = QLabel("Get Started")
        title.setFont(QFont("Times New Roman", 20, QFont.Bold))
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        user_label = QLabel("Username/Email")
        user_label.setFont(QFont("Times New Roman", 14))
        user_label.setStyleSheet("color: white;")
        layout.addWidget(user_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setStyleSheet("padding: 8px; font-size: 14px;")
        layout.addWidget(self.username_input)

        pass_label = QLabel("Password")
        pass_label.setFont(QFont("Times New Roman", 14))
        pass_label.setStyleSheet("color: white;")
        layout.addWidget(pass_label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setStyleSheet("padding: 8px; font-size: 14px;")
        layout.addWidget(self.password_input)

        login_btn = QPushButton("Login")
        login_btn.setStyleSheet(
            "background-color: red; color: white; font-weight: bold; padding: 8px;")
        login_btn.clicked.connect(self.login)
        layout.addWidget(login_btn)

        forgot_btn = QPushButton("Forget Password")
        forgot_btn.setStyleSheet(
            "background-color: transparent; color: white; font-size: 12px; padding: 4px;")
        layout.addWidget(forgot_btn)

        register_btn = QPushButton("New user Register")
        register_btn.setStyleSheet(
            "background-color: transparent; color: white; font-size: 12px; padding: 4px;")
        register_btn.clicked.connect(self.open_register)
        layout.addWidget(register_btn)

        self.login_frame.setLayout(layout)

     def login(self):
        email = self.username_input.text()
        password = self.password_input.text()


        if email == "" or password == "":
            messagebox.showerror("Error", "All fields are required")
            return

        login_data = {
            "type": "login",
            "email": email,
            "password": password
        }

        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((SERVER_HOST, SERVER_PORT))

            json_data = json.dumps(login_data)
            client.sendall(json_data.encode('utf-8'))

            response = client.recv(1024).decode('utf-8')
            client.close()

            if "successful" in response.lower():
                messagebox.showinfo("Login", response)
                self.register_dialog = RemoteFileManager()
                self.register_dialog.show()
            else:
                messagebox.showerror("Login Failed", response)

        except ConnectionRefusedError:
            messagebox.showerror("Connection Error", "Cannot connect to the server. Please check the network/server.")

    def open_register(self):
        self.register_dialog = RegistrationPage(self)
        self.register_dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())

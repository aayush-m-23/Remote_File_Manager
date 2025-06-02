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

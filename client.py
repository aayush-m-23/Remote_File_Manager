from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QLabel,
    QFileDialog, QMessageBox, QInputDialog, QProgressBar, QDialog, QTextEdit,
    QDialogButtonBox, QTableWidget, QTableWidgetItem, QLineEdit
)
from PySide6.QtCore import Qt, QTimer
import os
import socket
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from tkinter import ttk
import json
import sys

SERVER_HOST = '192.168.1.36'
SERVER_PORT = 5050
BUFFER_SIZE = 65536


class RemoteFileManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Remote File Manager")
        self.setMinimumSize(1000, 600)
        self.sock = None

        self.init_ui()
        self.connect_to_server()
        self.refresh_file_list()

    def init_ui(self):
        main_layout = QHBoxLayout(self)

        left_panel = QFrame()
        left_panel.setFrameShape(QFrame.StyledPanel)
        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.buttons = {
            "Refresh": self.refresh_file_list,
            "Upload": self.upload_file,
            "Download": self.download_file,
            "Delete": self.delete_file,
            "Rename": self.rename_file,
            "Open File":self.read_file,
        }

        for label, func in self.buttons.items():
            btn = QPushButton(label)
            btn.setFixedHeight(40)
            btn.clicked.connect(func)
            left_layout.addWidget(btn)

        self.progress = QProgressBar()
        self.progress.setFixedHeight(20)
        self.progress.setValue(0)
        self.progress.hide()
        left_layout.addWidget(self.progress)

        left_panel.setLayout(left_layout)

        right_panel = QFrame()
        right_panel.setFrameShape(QFrame.StyledPanel)
        right_layout = QVBoxLayout()

        label = QLabel("Remote Files")
        label.setStyleSheet("font-weight: bold; font-size: 16px;")

        search_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search files...")
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_files)
        search_layout.addWidget(self.search_bar)
        search_layout.addWidget(search_button)

        right_layout.addLayout(search_layout)


        self.file_table = QTableWidget(0, 1)
        self.file_table.setHorizontalHeaderLabels(["File Name"])
        self.file_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.file_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.file_table.horizontalHeader().setStretchLastSection(True)

        right_layout.addWidget(label)
        right_layout.addWidget(self.file_table)
        right_panel.setLayout(right_layout)

        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 3)

    def connect_to_server(self):
        try:
            self.sock = socket.socket()
            self.sock.connect((SERVER_HOST, SERVER_PORT))
        except Exception as e:
            QMessageBox.critical(self, "Connection Error", str(e))
            self.close()

    def send_command(self, cmd):
        try:
            self.sock.send(cmd.encode())
        except Exception as e:
            QMessageBox.critical(self, "Command Error", str(e))


    def send_json_command(self, command_dict):
        try:
            self.sock.send(json.dumps(command_dict).encode())
            response = self.sock.recv(BUFFER_SIZE).decode()
            return json.loads(response)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            return None

    def refresh_file_list(self):
        response = self.send_json_command({"action": "list"})
        if response and response["status"] == "ok":
            self.file_table.setRowCount(0)
            for filename in response["files"]:
                row = self.file_table.rowCount()
                self.file_table.insertRow(row)
                self.file_table.setItem(row, 0, QTableWidgetItem(filename))

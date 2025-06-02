import sys
import socket
import json
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QComboBox, QCheckBox,
    QPushButton, QGridLayout, QVBoxLayout, QMessageBox, QHBoxLayout, QDialog
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from tkinter import *
from tkinter import ttk, messagebox

class RegistrationPage(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("User Registration")
        self.setFixedSize(600, 600)
        self.setup_ui()

    def setup_ui(self):
        font_label = QFont("Arial", 11)
        font_title = QFont("Arial", 22, QFont.Bold)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(25)

        title = QLabel("Create Your Account")
        title.setFont(font_title)
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        form_layout = QGridLayout()
        form_layout.setHorizontalSpacing(20)
        form_layout.setVerticalSpacing(15)

        form_layout.addWidget(self.make_label("First Name:", font_label), 0, 0)
        self.fname_entry = QLineEdit()
        self.fname_entry.setPlaceholderText("Enter your first name")
        form_layout.addWidget(self.fname_entry, 0, 1)

        form_layout.addWidget(self.make_label("Last Name:", font_label), 0, 2)
        self.lname_entry = QLineEdit()
        self.lname_entry.setPlaceholderText("Enter your last name")
        form_layout.addWidget(self.lname_entry, 0, 3)

        form_layout.addWidget(self.make_label("Email:", font_label), 1, 0)
        self.email_entry = QLineEdit()
        self.email_entry.setPlaceholderText("Enter your email address")
        form_layout.addWidget(self.email_entry, 1, 1, 1, 3)

        form_layout.addWidget(self.make_label("Contact No.:", font_label), 2, 0)
        self.contact_entry = QLineEdit()
        self.contact_entry.setPlaceholderText("Enter your phone number")
        form_layout.addWidget(self.contact_entry, 2, 1, 1, 3)

        form_layout.addWidget(self.make_label("Password:", font_label), 3, 0)
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.setPlaceholderText("Enter password")
        form_layout.addWidget(self.password_entry, 3, 1)

        form_layout.addWidget(self.make_label("Confirm Password:", font_label), 3, 2)
        self.confirm_pass_entry = QLineEdit()
        self.confirm_pass_entry.setEchoMode(QLineEdit.Password)
        self.confirm_pass_entry.setPlaceholderText("Re-enter password")
        form_layout.addWidget(self.confirm_pass_entry, 3, 3)

        form_layout.addWidget(self.make_label("Security Question:", font_label), 4, 0)
        self.security_ques_combo = QComboBox()
        self.security_ques_combo.addItems([
            "Select",
            "Your Birth Place",
            "Your Birth Date",
            "Your Pet Name",
            "Your Favourite Movie"
        ])
        form_layout.addWidget(self.security_ques_combo, 4, 1, 1, 3)

        form_layout.addWidget(self.make_label("Security Answer:", font_label), 5, 0)
        self.ans_entry = QLineEdit()
        self.ans_entry.setPlaceholderText("Answer to your security question")
        form_layout.addWidget(self.ans_entry, 5, 1, 1, 3)

        main_layout.addLayout(form_layout)

        self.terms_check = QCheckBox("I agree to the Terms & Conditions")
        main_layout.addWidget(self.terms_check)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.register_btn = QPushButton("Register")
        self.register_btn.setFixedWidth(120)
        self.register_btn.clicked.connect(self.register)
        btn_layout.addWidget(self.register_btn)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setFixedWidth(120)
        self.cancel_btn.clicked.connect(self.close)
        btn_layout.addWidget(self.cancel_btn)

        main_layout.addLayout(btn_layout)

        self.setStyleSheet("""
            QLabel {
                font-size: 13px;
            }
            QLineEdit, QComboBox {
                font-size: 13px;
                padding: 6px;
            }
            QPushButton {
                font-size: 14px;
                padding: 8px;
                background-color: #2E8B57;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #246b45;
            }
            QCheckBox {
                font-size: 12px;
            }
        """)

    def make_label(self, text, font):
        lbl = QLabel(text)
        lbl.setFont(font)
        return lbl

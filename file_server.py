import socket
import threading
import json
import mysql.connector
import os

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5050
BUFFER_SIZE = 65536
FILE_STORAGE_PATH = "server_files"
os.makedirs(FILE_STORAGE_PATH, exist_ok=True)

db_config = {+
    "host": "localhost",
    "user": "root",
    "password": "Cailin#26",
    "database": "registration_db"
}

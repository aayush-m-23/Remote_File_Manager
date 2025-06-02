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

def insert_user(user_data):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (first_name, last_name, email, contact, password, security_question, security_answer)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            user_data["first_name"],
            user_data["last_name"],
            user_data["email"],
            user_data["contact"],
            user_data["password"],
            user_data["security_question"],
            user_data["security_answer"]
        ))
        conn.commit()
        return {"status": "ok", "message": "Registration successful"}
    except mysql.connector.IntegrityError as e:
        return {"status": "error", "message": "Email already registered"}
    except Exception as e:
        return {"status": "error", "message": f"DB error: {str(e)}"}
    finally:
        cursor.close()
        conn.close()

def validate_login(data):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE email=%s", (data["email"],))
        result = cursor.fetchone()
        if result and result[0] == data["password"]:
            return {"status": "ok", "message": "Login successful"}
        else:
            return {"status": "error", "message": "Invalid email or password"}
    except Exception as e:
        return {"status": "error", "message": f"DB error: {str(e)}"}
    finally:
        cursor.close()
        conn.close()

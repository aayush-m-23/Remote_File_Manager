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

def handle_file_command(client_socket, command):
    action = command.get("action")

    try:
        if action == "upload":
            filename = command["filename"]
            filesize = command["filesize"]
            filepath = os.path.join(FILE_STORAGE_PATH, filename)

            client_socket.send(json.dumps({"status": "ready"}).encode())
            with open(filepath, "wb") as f:
                total = 0
                while total < filesize:
                    chunk = client_socket.recv(min(BUFFER_SIZE, filesize - total))
                    if not chunk:
                        break
                    f.write(chunk)
                    total += len(chunk)
            client_socket.send(json.dumps({"status": "ok"}).encode())

        elif action == "download":
            filename = command["filename"]
            filepath = os.path.join(FILE_STORAGE_PATH, filename)
            if os.path.exists(filepath):
                with open(filepath, "rb") as f:
                    client_socket.sendfile(f)
            else:
                client_socket.send(json.dumps({"status": "error", "message": "File not found"}).encode())

        elif action == "delete":
            filename = command["filename"]
            filepath = os.path.join(FILE_STORAGE_PATH, filename)
            if os.path.exists(filepath):
                os.remove(filepath)
                client_socket.send(json.dumps({"status": "ok"}).encode())
            else:
                client_socket.send(json.dumps({"status": "error", "message": "File not found"}).encode())

        elif action == "rename":
            old_name = command["old_name"]
            new_name = command["new_name"]
            old_path = os.path.join(FILE_STORAGE_PATH, old_name)
            new_path = os.path.join(FILE_STORAGE_PATH, new_name)
            if os.path.exists(old_path):
                os.rename(old_path, new_path)
                client_socket.send(json.dumps({"status": "ok"}).encode())
            else:
                client_socket.send(json.dumps({"status": "error", "message": "File not found"}).encode())

        elif action == "search":
            query = command["query"]
            files = os.listdir(FILE_STORAGE_PATH)
            matching = [f for f in files if query.lower() in f.lower()]
            client_socket.send(json.dumps({"status": "ok", "files": matching}).encode())

        elif action == "list":
            files = os.listdir(FILE_STORAGE_PATH)
            client_socket.send(json.dumps({"status": "ok", "files": files}).encode())

        elif action == "read":
            filename = command["filename"]
            filepath = os.path.join(FILE_STORAGE_PATH, filename)
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                client_socket.send(json.dumps({"status": "ok", "content": content}).encode())
            else:
                client_socket.send(json.dumps({"status": "error", "message": "File not found"}).encode())

        else:
            client_socket.send(json.dumps({"status": "error", "message": "Invalid action"}).encode())

    except Exception as e:
        client_socket.send(json.dumps({"status": "error", "message": str(e)}).encode())

def handle_client(client_socket, address):
    print(f"[NEW CONNECTION] {address} connected.")
    try:
        while True:
            data = client_socket.recv(BUFFER_SIZE).decode()
            if not data:
                break
            try:
                command = json.loads(data)
            except json.JSONDecodeError:
                client_socket.send(json.dumps({"status": "error", "message": "Invalid JSON"}).encode())
                continue

            if command.get("type") == "register":
                response = insert_user(command)
                client_socket.send(json.dumps(response).encode())
            elif command.get("type") == "login":
                response = validate_login(command)
                client_socket.send(json.dumps(response).encode())
            elif command.get("action"):
                handle_file_command(client_socket, command)
            else:
                client_socket.send(json.dumps({"status": "error", "message": "Invalid request"}).encode())

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        client_socket.close()
        print(f"[DISCONNECTED] {address} disconnected.")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_HOST, SERVER_PORT))
    server.listen(5)
    print(f"[LISTENING] Server is listening on {SERVER_HOST}:{SERVER_PORT}")
    while True:
        client_socket, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()

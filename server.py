import socket
import threading
import time

HEADER = 64
PORT = 5555
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# Establish the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = []
messages = []
messages_lock = threading.Lock()

# Manages the incoming and outgoing messages related to each client
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    clients.append(conn)

    with messages_lock:
        for msg in messages:
            conn.send(msg.encode(FORMAT))
            time.sleep(0.1)

    connected = True
    while connected:
        try:
            message_length = conn.recv(HEADER).decode(FORMAT)
        except ConnectionResetError:
            pass
        if message_length:
            message_length = int(message_length)
            try:
                message = conn.recv(message_length).decode(FORMAT)
            except: pass
            if message == DISCONNECT_MESSAGE:
                connected = False
            else:
                messages.append(message)

            print(f"[{addr}] {message}")

            for client in clients:
                if client != conn:
                    try:
                        client.send(message.encode(FORMAT))
                    except ConnectionResetError:
                        pass
    clients.remove(conn)                    
    conn.close()

# Start the server and create a new thread for every client that connects
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.daemon = True
        thread.start()
        print(f" [ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] server is starting")
start()

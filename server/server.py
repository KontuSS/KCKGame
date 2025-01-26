import socket
import threading
from database.server_db import *

# Server settings
HOST = '127.0.0.1'
PORT = 12345

# Networking
clients = []

def broadcast(message, exclude_client=None):
    """Send a message to all clients except the sender."""
    for client in clients:
        if client != exclude_client:
            client.sendall(message.encode('utf-8'))

def handle_client(client, address):
    """Handle communication with an individual client."""
    print(f"New connection: {address}")

    # Receive client's ID
    client.sendall("Send your ID:".encode('utf-8'))
    client_id = client.recv(1024).decode('utf-8')

    # Retrieve client information from the database
    client_info = get_client_from_db(client_id)
    if client_info:
        client.sendall(f"Welcome {client_info[1]} from {client_info[2]} department!".encode('utf-8'))
    else:
        client.sendall("Client not found in database.".encode('utf-8'))

    try:
        while True:
            message = client.recv(1024).decode('utf-8')
            if not message:
                break

            print(f"Message from {address}: {message}")
            broadcast(message, exclude_client=client)
    except ConnectionResetError:
        print(f"Client {address} disconnected abruptly.")
    finally:
        clients.remove(client)
        client.close()
        print(f"Connection with {address} closed.")

def start_server():
    """Start the server."""
    setup_database()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(4)
    print(f"Server started on {HOST}:{PORT}")

    try:
        while True:
            client, address = server.accept()
            threading.Thread(target=handle_client, args=(client, address)).start()
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()
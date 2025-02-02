import socket
import threading
import sys
import os
import time
import json

# Add the project root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from database.server_db import *

# Server settings
# HOST = '10.128.134.128' # <- IP address on my pc on edurom
HOST = '127.0.0.1'
PORT = 12345

# Networking
clients = []
clientsID = []

def broadcast_single_client(obj, client_index):
    jsonStr = json.dumps(obj.__dict__)
    for i, client in enumerate(clients):
        if i == client_index:
            client.sendall(jsonStr.encode('utf-8'))

def broadcast(obj, exclude_client=None):
    """Send a message to all clients."""
    jsonStr = json.dumps(obj.__dict__)
    for client in clients:
        client.sendall(jsonStr.encode('utf-8'))

def handle_client(client, address):
    """Handle communication with an individual client."""
    print(f"New connection: {address}")    
    clients.append(client)
    
    # Receive client's ID
    client_id = client.recv(1024).decode('utf-8')
    clientsID.append(client_id)
    
    # Retrieve client information from the database
    client_info = get_player_by_id(client_id)
    
    if client_info:
        client.sendall(f"Welcome {client_info[1]} from {client_info[2]} department!".encode('utf-8'))
    else:
        client.sendall("Client not found in database.".encode('utf-8'))

    try:
        while True:
            time.sleep(4)
            pass
    except ConnectionResetError:
        print(f"Client {address} disconnected abruptly.")
    finally:
        clients.remove(client)
        clientsID.remove(client_id)
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
            # .accept() listens for new clients
            client, address = server.accept()
            threading.Thread(target=handle_client, args=(client, address)).start()
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        server.close()
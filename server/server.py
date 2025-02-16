import socket
import threading
import sys
import os
import time
import json
print("Server is running...")
# Add the project root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from database.server_db import *
from database.client_db import *

# Server settings
HOST = '192.168.18.71' # <- IP address on my pc on edurom
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
    for i, client in enumerate(clients):
        cards = get_player_cards(clientsID[i])
        if cards != None and cards[0] != None:
            obj.set_player_cards(cards[0])

        jsonStr = json.dumps(obj.__dict__)

        print(jsonStr)
        print(cards)
        client.sendall(jsonStr.encode('utf-8'))

def handle_client(client, address):
    """Handle communication with an individual client."""
    print(f"New connection: {address}")    
    clients.append(client)
    
    # Receive client's ID
    name = client.recv(1024).decode('utf-8')
    client_id = generate_client_info(name)
    clientsID.append(client_id[0])
    
    # Retrieve client information from the database
    print(f"id: {client_id[0]}")
    client.sendall(str(client_id[0]).encode('utf-8'))
    
    client.sendall(f"Welcome {name}!".encode('utf-8'))


    try:
        while True:
            try:
                time.sleep(4)
                pass                
            except (ConnectionResetError, BrokenPipeError):
                print(f"Client {address} disconnected unexpectedly.")
                break
    except (ConnectionResetError, BrokenPipeError):
        print(f"Client {address} disconnected unexpectedly.")
    finally:
        if client in clients:
            clients.remove(client)
        if client_id in clientsID:
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

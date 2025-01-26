import socket
from database.client_db import *

# Server connection settings
HOST = '127.0.0.1'
PORT = 12345

def start_client():
    """Start the client and send its information to the server."""
    setup_client_database()

    # Check if client info already exists
    client_info = get_client_info()
    if not client_info:
        client_id, name, department = generate_client_info()
        print(f"Generated Client: ID={client_id}, Name={name}, Department={department}")
    else:
        client_id, name, department = client_info
        print(f"Existing Client: ID={client_id}, Name={name}, Department={department}")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    # Send client ID to server
    client.sendall(str(client_id).encode('utf-8'))

    # Receive welcome message from server
    welcome_message = client.recv(1024).decode('utf-8')
    print(f"Server: {welcome_message}")

    try:
        while True:
            message = input("You: ")
            if message.lower() == 'quit':
                print("Disconnecting...")
                break

            client.sendall(message.encode('utf-8'))
    except KeyboardInterrupt:
        print("Client shutting down.")
    finally:
        client.close()

if __name__ == "__main__":
    start_client()
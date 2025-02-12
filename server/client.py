import socket
import sys
import os
import time
import json

# Add the project root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from database.client_db import *
# Server connection settings
# HOST = '10.128.134.128' # <- IP address on my pc on edurom
HOST = '10.128.157.223'
PORT = 12345
client_id = 0
client = None
global dto
dto = None

class MainDTO(object):
    whichPlayerTurn = None
    ectsInPool = 0
    highestEctsToMatch = 0
    lastPlayerId = None
    lastPlayerAction = None
    gameState = 0
    playerCards = ''
    cardsOnTable = ''

    def __init__(self, whichPlayerTurn=None, ectsInPool=0, highestEctsToMatch=0, 
                 lastPlayerId=None, lastPlayerAction=None, gameState=None, 
                 playerCards='', cardsOnTable=''):
        self.whichPlayerTurn = whichPlayerTurn
        self.ectsInPool = ectsInPool
        self.highestEctsToMatch = highestEctsToMatch
        self.lastPlayerId = lastPlayerId
        self.lastPlayerAction = lastPlayerAction
        self.gameState = gameState
        self.playerCards = playerCards
        self.cardsOnTable = cardsOnTable
def return_client_id():
    return client_id

def return_dto():
    global dto
    if dto is not None:
        print(f"dto: {dto.playerCards} cline.py")
    else:
        print('dto is None client.py')
    return dto

def start_client(name):
    """Start the client and send its information to the server."""

    # Check if client info already exists
    # client_info = get_client_info()
    # if not client_info:
    #     client_id, name, department = generate_client_info()
    #     print(f"Generated Client: ID={client_id}, Name={name}, Department={department}")
    # else:
    #     client_id, name, department = client_info
    #     print(f"Existing Client: ID={client_id}, Name={name}, Department={department}")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    # Send client ID to server
    client.sendall(name.encode('utf-8'))

    client_id = client.recv(1024).decode('utf-8')

    # Receive welcome message from server
    welcome_message = client.recv(1024).decode('utf-8')
    print(f"Server: {welcome_message}")        

    try:
        while True:
            while True:
                message = client.recv(2024).decode('utf-8')
                if(message != None):
                    print(f"Server: {message}")
                    dto_temp = MainDTO(**json.loads(message))
                    global dto
                    if dto_temp is not None:
                        dto = dto_temp
                        print(f"dto: is set")
               
                    print(f"dto: {dto.playerCards}")

                    if str(dto.whichPlayerTurn) == str(client_id):
                        print('ASK FOR CLIENT INPUT')
                        break
                    
                time.sleep(1)

            
          

           # client.sendall(client_input.encode('utf-8'))
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("Client shutting down.")
    finally:
        client.close()

if __name__ == "__main__":
    start_client(None)
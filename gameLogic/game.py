import random
import sys
import os
import socket
import threading
import time

# NAJWAŻNIEJSZE TODO

# 1. Wystawić server zeby mozna było wysyłać z niego requesty i broadcasty

# Ad. 1 pomysł: dać w serverze wątek na stałe śledzenie tabeli 'game' i wysyłanie requestów i broadcastów zaleznie od
# zmiany w danej krotce

# 2. Zrobić test na wszystkie zapytania do bazy danych czy wszystko jest git

# 3. Zasymulować odpalenie na różnych komputerach

# 4.* Przerobienie/Dorobienie obiektowości i zrobienie z player/server/obsługi klas z metodami i atrybutami
# *Nie wiadomo czy potrzebne może sie przyda

# Add the project root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from database.server_db import *
from database.client_db import *
from server.server import broadcast, start_server, clients, clientsID
from enum import Enum

class PlayerActions(Enum):
    BET = '1'
    CALL = '2'
    CHECK = '3'
    FOLD = '4'
    AWAIT = '5'

class GameState(Enum):
    STARTING = 1
    PROGRESS = 2
    
    TURN1 = 3
    TURN2 = 4
    TURN3 = 5
    TURN4 = 6
    
    FINISHED = 7

# Card Deck
SUITS = ['H', 'D', 'C', 'S']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

DECK = [f"{rank}{suit}" for suit in SUITS for rank in RANKS]
random.shuffle(DECK)


# Function to obtain single card from deck and remove it from deck
def get_single_card():
    card = DECK.pop()
    return card

# Deal cards to players
def deal_cards(players, game_id):

    # Assign 2 cards to each player
    for player in players:
        hand = ', '.join([get_single_card(), get_single_card()])  # Deal 2 cards per player
        print(f"Hand: {hand}")
        hand_strength = evaluate_hand(hand)
        save_hand(game_id, player, hand, hand_strength)

# Evaluate hand strength (simple logic for now)
def evaluate_hand(hand):
    cards = hand.split(', ')
    ranks = [card.split(' ')[0] for card in cards]
    
    # Check if all ranks are the same (simplified check for pairs)
    if len(set(ranks)) == 1:
        return "Pair"
    elif len(set(ranks)) == 2:
        return "Full House"
    else:
        return "High Card"

def player_action(player_id, action_type):
    set_player_state(player_id, action_type)
    #define what it does further

    return action_type


def check_players_status(players):
    for i in players:
        current_action = get_player_state(players[i])
        if current_action == 5:
            return False


def deal_cards_on_table(game_state, table_hand):
    if game_state == GameState.TURN1.value:
        return table_hand
    elif game_state == GameState.TURN2.value:
        table_hand = ', '.join([get_single_card(), get_single_card(), get_single_card()])
    elif game_state == GameState.TURN3.value:
        table_hand+=", "+get_single_card()
    elif game_state == GameState.TURN4.value:
        table_hand+=", "+get_single_card()
    else:
        print("Not valid game state type provided")        
    return table_hand

def process_player_action(action, current_player_socket, current_player_id, betAmount, game_id):
    if action == PlayerActions.CHECK.value:
        broadcast(f"Player {current_player_id} has checked.")
        return True
    
    elif action == PlayerActions.FOLD.value:
        broadcast(f"Player {current_player_id} has folded.")
        player_fold(current_player_id)
        return True
    
    elif action == PlayerActions.BET.value:
        broadcast(f"Player {current_player_id} has betted.")
        player_bet(current_player_id, game_id, betAmount)
        return True
    
    elif action == PlayerActions.CALL.value:
        broadcast(f"Player {current_player_id} has called.")
        player_call(current_player_id, game_id)
        return True
    else:
        print("Not valid action type provided")
    

#template game loop, need to link to db and server action
def game_loop():
    time.sleep(2)
    print('Waiting for players!')
    while len(clientsID)<2:
        time.sleep(2)
        pass
    
    DECK = [f"{rank}{suit}" for suit in SUITS for rank in RANKS]
    random.shuffle(DECK)
    
    print("Game is starting!")
    
    # Add starting state to DB
    add_new_game()
    # It created new gameID, fetch this ID
    game_id = get_latest_game_id()
    print(f"GameID: {game_id}")
    # Fetch all currently connected players
    players = clientsID
    playerCount = len(players)
    playerTurn = 0
    print(f"players table: {players}")
    
    print("The game is starting! BroadCast")
    broadcast("The game is starting!")
    # Set first player ID
    first_player_id = players[playerTurn]
    # Modify games table in DB
    start_game(game_id, first_player_id)
    
    DEVELOP_game_state = 3
    
    deal_cards(players, game_id)
    table_hand = ''
    #MAIN GAME LOOP \/
    while True:
        game_state = get_game_state(game_id)
        if game_state[0] == GameState.FINISHED.value:
                break        
        print(f"game state: {game_state}")
        table_hand = deal_cards_on_table(game_state[0], table_hand)
        print(f"Cards on table: {table_hand}")
        #TRUN LOOP
        while True:                   
            current_player_socket = clients[playerTurn]
            current_player_id = get_current_player(game_id)
            print(f"Player ID:{current_player_id[0]} turn")
            broadcast(f"Player {current_player_id[0]} turn")
            
            # PLAYER ACTIONS IN TURN LOOP       
            # Listen to player action
            #print("Listetning to player action")
            action = str(current_player_socket.recv(1024).decode('utf-8'))
                # :fold
                # :bet x
                # :call
                # :check
            try:
                betAmount = action.split(" ")[1]
                action = action.split(" ")[0]
                print(f"Bet amout: {betAmount}")
            except:
                betAmount = 0
                
                    
            print(f"Player Action: {action}") 
            
                
            process_player_action(action, current_player_socket, current_player_id[0], betAmount, game_id)

            # For this example, just rotate between players
            playerTurn+=1
            if playerTurn >= playerCount:
                playerTurn=0
            next_player = players[playerTurn]
            
            #print(f"next player: {next_player}")
            if next_player==first_player_id: break            
            set_next_player(next_player, game_id)
        # After turn
        DEVELOP_game_state+=1
        update_game_state(game_id, DEVELOP_game_state)
        ectsPool = get_ectsPool(game_id)
        print(f"Current ects pool: {ectsPool}")
        
    print("Game ended, start new game!")
            

if __name__ == "__main__":
    threading.Thread(target=game_loop).start()
    start_server()

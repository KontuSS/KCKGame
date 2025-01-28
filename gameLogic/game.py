import random
import sys
import os
import socket

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
from server.server import broadcast, clients
from enum import Enum

class PlayerActions(Enum):
    BET = 1
    CALL = 2
    CHECK = 3
    FOLD = 4
    AWAIT = 5

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
    for i, player in enumerate(players):
        hand = ', '.join([get_single_card(), get_single_card()])  # Deal 2 cards per player
        hand_strength = evaluate_hand(hand)
        save_hand(game_id, player['id'], hand, hand_strength)

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
    for player in enumerate(players):
        current_action = get_player_state(player['id'])
        if current_action == 5:
            return False


def deal_cards_on_table(game_state, table_hand):
    if game_state == GameState.TURN1:
        return
    elif game_state == GameState.TURN2:
        table_hand += ', '.join(DECK[0:3])  # Deal 3 cards on table
    elif game_state == GameState.TURN3:
        table_hand += ', '.join(DECK[0:1]) # Deal 1 cards on table
    elif game_state == GameState.TURN4:
        table_hand += ', '.join(DECK[0:1]) # Deal 1 cards on table

#template game loop, need to link to db and server action
def game_loop():
    
    # Prepare game
    
    # Add starting state to DB
    add_new_game()
    # It created new gameID, fetch this ID
    game_id = get_latest_game_id()
    # Fetch all currently connected players
    players = get_all_clients()
    
    print("Starting a new game...")
    broadcast("The game is starting!")
    # Set first player ID
    first_player_id = players[0]['id']
    # Modify games table in DB
    start_game(game_id, first_player_id)
    
    deal_cards(players, game_id)
    
    #MAIN GAME LOOP \/
    while True:
        game_state = get_game_state(game_id)
        if game_state == GameState.FINISHED:
                break        
        deal_cards_on_table(game_state)
        #TRUN LOOP
        while True:                   
            current_player_socket = clients[0]
            current_player_id = get_current_player(game_id)        
            broadcast(f"Player {current_player_id}'s turn")
            
            # PLAYER ACTIONS IN TURN LOOP       
            while True:
                # Listen to player action
                action = current_player_socket.client.recv(1024).decode('utf-8')
                
                if action == PlayerActions.FOLD:
                    broadcast(f"Player {current_player_id} has folded.")
                    break
                elif action == PlayerActions.BET:
                    broadcast(f"Player {current_player_id} has placed a bet.")
                    break
                elif action == PlayerActions.CALL:
                    broadcast(f"Player {current_player_id} has called the bet.")
                    break
                elif action == PlayerActions.CHECK:
                    

            # KALKULACJE PULI / WARTOSCI / SIŁY KART GRACZY

            # For this example, just rotate between players
            next_player = (current_player_id % len(players)) + 1
            set_next_player(next_player)
            
            #if when all players will do sth then break
            
        #game state upda
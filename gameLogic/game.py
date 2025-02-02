import random
import sys
import os
import socket
import threading
import time
import json


# NAJWAŻNIEJSZE TODO

# *Przerobienie/Dorobienie obiektowości i zrobienie z player/server/obsługi klas z metodami i atrybutami
# *Nie wiadomo czy potrzebne może sie przyda

# Add the project root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from database.server_db import *
from database.client_db import *
from server.server import broadcast, start_server, broadcast_single_client, clients, clientsID
from enum import Enum

class PlayerActions(Enum):
    BET = '1'
    CALL = '2'
    CHECK = '3'
    FOLD = '4'

class GameState(Enum):
    WAITING = 1
    STARTING = 2
    
    TURN1 = 3
    TURN2 = 4
    TURN3 = 5
    TURN4 = 6
    
    FINISHED = 7

class MainDTO(object):
    whichPlayerTurn = None
    ectsInPool = 0
    highestEctsToMatch = 0
    lastPlayerId = None
    lastPlayerAction = None
    gameState = 1
    playerCards = ''
    cardsOnTable = ''

    def reset_game(self):
        self.whichPlayerTurn = None
        self.ectsInPool = 0
        self.highestEctsToMatch = 0
        self.lastPlayerId = None
        self.lastPlayerAction = None
        self.gameState = GameState.WAITING
        self.playerCards = ''
        self.cardsOnTable = ''

    def set_which_player_turn(self, player_turn):
        self.whichPlayerTurn = player_turn

    def set_ects_in_pool(self, ects):
        self.ectsInPool = ects

    def set_highest_ects_to_match(self, ects):
        self.highestEctsToMatch = ects

    def set_last_player_id(self, player_id):
        self.lastPlayerId = player_id

    def set_last_player_action(self, action):
        self.lastPlayerAction = action

    def set_game_state(self, game_state):
        self.gameState = game_state

    def set_player_cards(self, cards):
        self.playerCards = cards

    def set_cards_on_table(self, cards):
        self.cardsOnTable = cards

# game data

# Card Deck
SUITS = ['H', 'D', 'C', 'S']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
DECK = [f"{rank}{suit}" for suit in SUITS for rank in RANKS]

# main data transfer object
game = MainDTO()

# Function to obtain single card from deck and remove it from deck
def get_single_card():
    card = DECK.pop()
    return card

# Deal cards to players
def deal_cards(players, game_id):

    # Assign 2 cards to each player
    for i, player in enumerate(players):
        hand = ', '.join([get_single_card(), get_single_card()])  # Deal 2 cards per player
        print(f"Hand: {hand}")
        hand_strength = evaluate_hand(hand)
        save_hand(game_id, player, hand, hand_strength)
        game.set_player_cards(hand)
        broadcast_single_client(game, i)
        game.set_player_cards('')


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
        game.set_cards_on_table(table_hand)
        broadcast(game)
    elif game_state == GameState.TURN3.value:
        table_hand+=", "+get_single_card()
        game.set_cards_on_table(table_hand)
        broadcast(game)
    elif game_state == GameState.TURN4.value:
        table_hand+=", "+get_single_card()
        game.set_cards_on_table(table_hand)
        broadcast(game)
    else:
        print("Not valid game state type provided")        
    return table_hand

def process_player_action(action, current_player_socket, current_player_id, betAmount, game_id):
    game.set_last_player_id(current_player_id)
    game.set_which_player_turn(None)
    if action == PlayerActions.CHECK.value:
        game.set_last_player_action(PlayerActions.CHECK.value)
        broadcast(game)
        return True
    
    elif action == PlayerActions.FOLD.value:
        game.set_last_player_action(PlayerActions.FOLD.value)   
        broadcast(game)
        player_fold(current_player_id)
        return True
    
    elif action == PlayerActions.BET.value:
        betAmountInt = int(betAmount)
        game.set_last_player_action(PlayerActions.BET.value)
        game.set_ects_in_pool(game.ectsInPool+betAmountInt)
        if(betAmountInt > game.highestEctsToMatch):
            game.set_highest_ects_to_match(betAmountInt)
        broadcast(game)
        player_bet(current_player_id, game_id, betAmount)
        return True
    
    elif action == PlayerActions.CALL.value:
        game.set_last_player_action(PlayerActions.CALL.value)
        broadcast(game)
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
    
    #DECK = [f"{rank}{suit}" for suit in SUITS for rank in RANKS]
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
    turnLenght = playerCount
    maxBet = 0
    print(f"players table: {players}")

    game.set_game_state(GameState.STARTING.value)
    broadcast(game)

    
    # Set first player ID
    first_player_id = players[playerTurn]
    # Modify games table in DB
    start_game(game_id, first_player_id)
    
    DEVELOP_game_state = 3
    
    deal_cards(players, game_id)
    table_hand = ''
    time.sleep(1)
    #MAIN GAME LOOP \/
    while True:
        game_state = get_game_state(game_id)
        if game_state[0] == GameState.FINISHED.value:
                break        
        print(f"game state: {game_state}")
        table_hand = deal_cards_on_table(game_state[0], table_hand)
        print(f"Cards on table: {table_hand}")
        time.sleep(1)
        #TURN LOOP
        while True:                   
            current_player_socket = clients[playerTurn]
            current_player_id = get_current_player(game_id)
            print(f"Player ID:{current_player_id[0]} turn")
            game.set_which_player_turn(int(current_player_id[0]))
            time.sleep(1)
            broadcast(game)
            
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
            
            #block bet under maxbet
            if action == PlayerActions.BET.value and betAmount>maxBet:
                maxBet = betAmount
                turnLenght = playerCount - 1
            
            
            time.sleep(1)

            # Rotate between players
            playerTurn+=1
            turnLenght-=1
            
            if playerTurn > (playerCount-1):
                playerTurn=0
                
            next_player = players[playerTurn]
            if turnLenght==0: break
                       
            set_next_player(next_player, game_id)
            
        # After turn
        DEVELOP_game_state+=1
        update_game_state(game_id, DEVELOP_game_state)
        ectsPool = get_ectsPool(game_id)
        print(f"Current ects pool: {ectsPool}")

        if(ectsPool == 50):
            # for player in players:
            #     evaluate_hand()
            break
        
    print("Game ended, start new game!")
            

if __name__ == "__main__":
    threading.Thread(target=game_loop).start()
    start_server()

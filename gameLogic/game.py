import random
import sys
import os

# Add the project root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from database.server_db import *
from database.client_db import *

# Defines
STATE_WAITING = "waiting"
STATE_PROGRESS = "in-progress"
STATE_FINISHED = "finished"

# Card Deck
SUITS = ['H', 'D', 'C', 'S']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

DECK = [f"{rank} of {suit}" for suit in SUITS for rank in RANKS]

# Deal cards to players
def deal_cards(players, game_id):
    deck = DECK.copy()
    random.shuffle(deck)

    # Assign 2 cards to each player
    for i, player in enumerate(players):
        hand = ', '.join(deck[i*2:i*2+2])  # Deal 2 cards per player
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

# Start a new game
def start_new_game(players):
    # Step 1: Add the game to the database
    add_new_game()

    # Step 2: Retrieve game_id from database
    game_id = get_latest_game_id()

    # Step 3: Deal cards to players
    deal_cards(players, game_id)

    # Step 4: Update the game state
    first_player_id = players[0]['id']
    start_game(game_id, first_player_id)

    return game_id

# Get the latest game ID (just an example)
def get_latest_game_id():
    conn = sqlite3.connect('client.db')
    cursor = conn.cursor()
    cursor.execute('SELECT game_id FROM games ORDER BY game_id DESC LIMIT 1')
    game_id = cursor.fetchone()[0]
    conn.close()
    return game_id


#template game loop, need to link to db and server action
def game_loop():
    # Step 1: Initialize the game (start new game, deal cards, etc.)
    players = get_all_players()
    game_id = 1  # Simulated game ID for this example

    # Start the game
    print("Starting a new game...")
    broadcast("The game is starting!")
    update_game_state(game_id, STATE_PROGRESS)
    
    # Step 2: Deal cards to players
    hands = deal_cards(players, game_id)

    # Step 3: Main game loop
    while True:
        game_state = get_game_state(game_id)
        
        if game_state == STATE_FINISHED:
            break  # End the game if it's finished
        
        # Step 3.1: Get current player
        current_player_id = get_current_player(game_id)
        print(f"Player {current_player_id}'s turn")
        
        # Step 3.2: Simulate player action (e.g., fold, bet, call)
        action = player_action(current_player_id, ACTION_BET)  # Example: player bets
        
        # Step 3.3: Handle action
        if action == ACTION_FOLD:
            broadcast_game_message(f"Player {current_player_id} has folded.")
            # In a real game, you'd remove the player from the active pool
        elif action == ACTION_BET:
            broadcast_game_message(f"Player {current_player_id} has placed a bet.")
        elif action == ACTION_CALL:
            broadcast_game_message(f"Player {current_player_id} has called the bet.")
        
        # Step 3.4: Check if all players have completed their actions
        # (for simplicity, we assume that after each player's turn, everyone acts)
        # Here you can check if all players have folded or called, or if a winner is determined.
        
        # Simulating next player turn
        time.sleep(1)  # Pause to simulate real-time game

        # For this example, just rotate between players
        next_player = (current_player_id % len(players)) + 1
        print(f"Next player is {next_player}")
        
        # Example: Game ends when players have finished their turns
        if all([True for _ in players]):  # Replace with actual check
            update_game_state(game_id, STATE_FINISHED)
            break
    
    # Step 4: Determine winner based on hands
    print("Game Over!")
    winner_id = 1  # Simulated winner ID for example
    print(f"Player {winner_id} wins the game!")
    
    
# Running the main game loop
if __name__ == '__main__':
    game_loop()
import random
import sys
import os

# Add the project root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from database.server_db import *

# Card Deck
SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
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
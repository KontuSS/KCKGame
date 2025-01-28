import sqlite3

DB_NAME = "clients.db"

def setup_database():
    """Create the clients tables if it doesn't already exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            action INTEGER,
            address TEXT NOT NULL
        )
    ''')
    conn.commit()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            game_id INTEGER PRIMARY KEY AUTOINCREMENT,
            state TEXT NOT NULL,  -- 'waiting', 'in-progress', 'finished'
            current_player_id INTEGER,  -- Points to player whos currently playing
            winner_id INTEGER  -- Points to the winning playerc
            )
    ''')
    conn.commit()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hands (
            hand_id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER,
            player_id INTEGER,
            cards TEXT,  -- Cards dealt to the player, stored as a comma-separated string
            hand_strength TEXT,  -- Strength of the player's hand (e.g., "Full House")
            FOREIGN KEY(game_id) REFERENCES games(game_id),
            FOREIGN KEY(player_id) REFERENCES players(id)
        )
    ''')    
    conn.commit()
    
    conn.close()

# def add_client_to_db(name, department):
#     """Add a new client to the database."""
#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()
#     cursor.execute('INSERT INTO clients (name, department) VALUES (?, ?)', (name, department))
#     conn.commit()
#     client_id = cursor.lastrowid
#     conn.close()
#     return client_id


#GameLoop database querries
def get_all_players():
    conn = sqlite3.connect('client.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, department FROM players')
    players = cursor.fetchall()
    conn.close()
    return players

def get_player_by_id(client_id):
    """Retrieve client information from the database by ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()    
    cursor.execute('SELECT id, name, department FROM players WHERE id = ?', (client_id,))
    client = cursor.fetchone()
    conn.close()
    return client

def get_game_state(game_id):
    """Retrieve game information from the database by ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()    
    cursor.execute('SELECT state FROM games WHERE game_id = ?', (game_id,))
    state = cursor.fetchone()    
    conn.close()
    return state

def get_current_player(game_id):
    """Retrieve current player from the database by game ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()    
    cursor.execute('SELECT current_player_id FROM games WHERE game_id = ?', (game_id,))
    state = cursor.fetchone()    
    conn.close()
    return state
    
#Game menagment and initalizers within database
def add_new_game():
    conn = sqlite3.connect('client.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO games (state) VALUES (?)', ('starting',))
    conn.commit()
    conn.close()

def start_game(game_id, first_player_id):
    conn = sqlite3.connect('client.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE games SET state = ?, current_player_id = ? WHERE game_id = ?',
                   ('in-progress', first_player_id, game_id))
    conn.commit()
    conn.close()
    
def update_game_state(game_id, game_state):
    conn = sqlite3.connect('client.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE games SET state = ? WHERE game_id = ?', (game_state, game_id))
    conn.commit()
    conn.close()

def get_latest_game_id():
    conn = sqlite3.connect('client.db')
    cursor = conn.cursor()
    cursor.execute('SELECT game_id FROM games ORDER BY game_id DESC LIMIT 1')
    game_id = cursor.fetchone()[0]
    conn.close()
    return game_id

# Player managment querries

def get_player_state(player_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()    
    cursor.execute('SELECT action FROM players WHERE id = ?', (player_id,))
    client = cursor.fetchone()
    conn.close()
    return client

def set_player_state(player_id, action_type):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()    
    cursor.execute('UPDATE players SET action = ? WHERE id = ?', (action_type, player_id))
    conn.commit()
    conn.close()  
    
def set_next_player(player_id):
    return 1
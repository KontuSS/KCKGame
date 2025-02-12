import sqlite3

DB_NAME = "game.db"

def setup_database():
    """Create the clients tables if it doesn't already exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            action INTEGER,
            state INTEGER, --playing:0 , folded:1,
            ectsPool INTEGER
        )
    ''')
    conn.commit()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            game_id INTEGER PRIMARY KEY AUTOINCREMENT,
            state INTEGER NOT NULL,  -- 
            current_player_id INTEGER,  -- Points to player whos currently playing
            winner_id INTEGER,  -- Points to the winning playerc
            turnPool INTEGER,
            currentBet INTEGER
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
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM players')
    players = cursor.fetchall()
    conn.close()
    return players

def get_player_by_id(client_id):
    """Retrieve client information from the database by ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()    
    cursor.execute('SELECT id, name FROM players WHERE id = ?', (client_id,))
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
    player = cursor.fetchone()    
    conn.close()
    return player
    
#Game menagment and initalizers within database
def add_new_game():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO games (state) VALUES (?)', (1,))
    conn.commit()
    conn.close()

def start_game(game_id, first_player_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('UPDATE games SET state = ?, current_player_id = ?, turnPool = ?, currentBet = ? WHERE game_id = ?',
                   (3, first_player_id, 0, 0, game_id))
    conn.commit()
    conn.close()
    
def update_game_state(game_id, game_state):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('UPDATE games SET state = ? WHERE game_id = ?', (game_state, game_id))
    conn.commit()
    conn.close()

def get_latest_game_id():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT game_id FROM games ORDER BY game_id DESC LIMIT 1')
    game_id = cursor.fetchone()[0]
    conn.close()
    return game_id

def get_ectsPool(gameId):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT turnPool FROM games WHERE game_id = ?', (gameId,))
    game_id = cursor.fetchone()
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
    
def set_next_player(player_id, game_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()    
    cursor.execute('UPDATE games SET current_player_id = ? WHERE game_id = ?', (player_id, game_id))
    conn.commit()
    conn.close()  

def player_fold(player_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('UPDATE players SET state = ? WHERE id = ?', (1, player_id))
    conn.commit()
    conn.close()
    
def player_bet(player_id, game_id, betAmmout):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT ectsPool from players WHERE id=?', (player_id,))
    ectsPool = cursor.fetchone()[0]
    ectsPool -= int(betAmmout)
    
    cursor.execute('UPDATE players SET ectsPool = ? WHERE id = ?', (ectsPool, player_id))
    conn.commit()
        
    cursor.execute('UPDATE games SET currentBet = ? WHERE game_id = ?', (betAmmout, game_id))
    conn.commit()
    
    cursor.execute('SELECT turnPool from games WHERE game_id=?',(game_id,))
    turnPool = cursor.fetchone()[0]
    turnPool += int(betAmmout)
    
    cursor.execute('UPDATE games SET turnPool = ? WHERE game_id = ?', (turnPool, game_id))
    conn.commit()
    
    conn.close()
    
def player_call(player_id, game_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT ectsPool from players WHERE id=?',(player_id,))
    ectsPool = cursor.fetchone()[0]
    
    cursor.execute('SELECT currentBet from games WHERE game_id=?',(game_id,))
    currentBet = cursor.fetchone()[0]    
    ectsPool -= currentBet
    
    cursor.execute('UPDATE players SET ectsPool = ? WHERE id = ?', (ectsPool, player_id))
    conn.commit()  
    
    cursor.execute('SELECT turnPool from games WHERE game_id=?',(game_id,))
    turnPool = cursor.fetchone()[0]
    turnPool += currentBet    
    
    cursor.execute('UPDATE games SET turnPool = ? WHERE game_id = ?', (turnPool, game_id))
    conn.commit()
    
    conn.close()

def get_player_cards(player_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()    
    cursor.execute('SELECT cards FROM hands WHERE player_id = ?', (player_id,))
    client = cursor.fetchone()
    conn.close()

    return client
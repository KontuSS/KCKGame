import sqlite3

DB_NAME = "clients.db"

def setup_database():
    """Create the clients table if it doesn't already exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            game_id INTEGER PRIMARY KEY AUTOINCREMENT,
            state TEXT NOT NULL,  -- 'waiting', 'in-progress', 'finished'
            current_player_id INTEGER,  -- Points to player who’s currently playing
            winner_id INTEGER  -- Points to the winning player
            )
    ''')
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
    
    print(f"DB LOG: CLIENT_ID: {client_id}")
    
    cursor.execute('SELECT id, name, department FROM clients WHERE id = ?', (client_id,))
    client = cursor.fetchone()
    
    print(f"DB LOG: CLIENT: {client}")
    
    conn.close()
    return client

def add_new_game():
    conn = sqlite3.connect('client.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO games (state) VALUES (?)', ('waiting',))
    conn.commit()
    conn.close()

def start_game(game_id, first_player_id):
    conn = sqlite3.connect('client.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE games SET state = ?, current_player_id = ? WHERE game_id = ?',
                   ('in-progress', first_player_id, game_id))
    conn.commit()
    conn.close()
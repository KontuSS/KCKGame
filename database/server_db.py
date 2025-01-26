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
    conn.commit()
    conn.close()

def add_client_to_db(name, department):
    """Add a new client to the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO clients (name, department) VALUES (?, ?)', (name, department))
    conn.commit()
    client_id = cursor.lastrowid
    conn.close()
    return client_id

def get_client_from_db(client_id):
    """Retrieve client information from the database by ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, department FROM clients WHERE id = ?', (client_id,))
    client = cursor.fetchone()
    conn.close()
    return client
import sqlite3

DB_NAME = "clients.db"

def generate_client_info():
    """Generate client information and store it locally."""
    name = input("Enter your name: ")
    department = input("Enter your department: ")

    # Store in local database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO clients (name, department) VALUES (?, ?)', (name, department))
    conn.commit()
    client_id = cursor.lastrowid
    conn.close()
    return client_id, name, department

# def get_client_info():
#     """Retrieve the client's information from the local database."""
#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()
#     cursor.execute('SELECT id, name, department FROM clients ORDER BY id DESC LIMIT 1')
#     client = cursor.fetchone()
#     conn.close()
#     return client
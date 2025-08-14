import sqlite3

def create_db():
    """Creates the database and items table if not exists."""
    conn = sqlite3.connect("expiry_tracker.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            expiry_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_item(name, expiry_date):
    """Inserts an item into the database."""
    conn = sqlite3.connect("expiry_tracker.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name, expiry_date) VALUES (?, ?)", (name, expiry_date))
    conn.commit()
    conn.close()

def get_items():
    """Fetches all stored items."""
    conn = sqlite3.connect("expiry_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, expiry_date FROM items")
    items = cursor.fetchall()
    conn.close()
    return items

# Initialize database
create_db()

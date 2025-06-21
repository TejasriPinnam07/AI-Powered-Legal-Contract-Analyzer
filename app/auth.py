import sqlite3
import hashlib
import os

# Path to store the users database
DB_PATH = os.path.join("users.db")

def init_db():
    """Create users table if not exists."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            email TEXT
        )
    ''')
    conn.commit()
    conn.close()

def make_hashes(password):
    """Hash password with SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()

def check_hashes(password, hashed_text):
    """Verify password against hash."""
    return make_hashes(password) == hashed_text

def add_user(username, password, email):
    """Insert a new user."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
              (username, make_hashes(password), email))
    conn.commit()
    conn.close()

def login_user(username, password):
    """Check if user credentials are valid."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT password FROM users WHERE username = ?', (username,))
    data = c.fetchone()
    conn.close()
    return data and check_hashes(password, data[0])

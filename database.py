import sqlite3
import bcrypt
from datetime import datetime, timedelta
import json

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def add_user(username, email, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # Hash password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Insert user
    try:
        c.execute(
            'INSERT INTO users (username, email, password_hash, created_at) VALUES (?, ?, ?, ?)',
            (username, email, password_hash.decode('utf-8'), datetime.utcnow().isoformat())
        )
        conn.commit()
        user_id = c.lastrowid
    except sqlite3.IntegrityError:
        return None  # User already exists
    finally:
        conn.close()
    
    return user_id

def get_user_by_username(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    
    if user:
        return {
            'id': user[0],
            'username': user[1],
            'email': user[2],
            'password_hash': user[3],
            'created_at': user[4]
        }
    return None

def get_user_by_id(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    conn.close()
    
    if user:
        return {
            'id': user[0],
            'username': user[1],
            'email': user[2],
            'password_hash': user[3],
            'created_at': user[4]
        }
    return None

def get_all_users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    c.execute('SELECT * FROM users')
    users = c.fetchall()
    conn.close()
    
    return [
        {
            'id': user[0],
            'username': user[1],
            'email': user[2],
            'created_at': user[4]
        }
        for user in users
    ]

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# Initialize database when this module is imported
init_db()
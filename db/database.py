import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "database.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    """Initialize the database connection"""
    conn = get_connection()
    try:
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        raise
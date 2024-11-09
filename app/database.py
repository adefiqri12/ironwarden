import sqlite3
import os

def init_db(db_name='db.sqlite3'):
    db_exists = os.path.exists(db_name)
    try:
        conn = sqlite3.connect(db_name)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        if not db_exists:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS master_accounts (
                master_username TEXT PRIMARY KEY,
                master_password BLOB
            )
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS stored_passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                site_name TEXT,
                salt BLOB,
                iv BLOB,
                encrypted_password BLOB,
                FOREIGN KEY (username) REFERENCES master_accounts(master_username)
            )
            ''')
            conn.commit()
        else:
            print("Database already exists")
        return conn, cursor
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None, None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None, None

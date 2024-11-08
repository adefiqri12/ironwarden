import sqlite3
import os

def init_db(db_name='password_manager.db'):
    # Check if the database file already exists
    db_exists = os.path.exists(db_name)
    
    try:
        # Connect to the database (create if not exists)
        conn = sqlite3.connect(db_name)
        # Enable foreign key support
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        
        # Initialize tables only if the database was just created
        if not db_exists:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                master_username TEXT PRIMARY KEY,
                hashed_password BLOB
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
                FOREIGN KEY (username) REFERENCES users(master_username)
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

import bcrypt
import sqlite3

# Create a new user (master username and hashed master password)
def create_user(cursor, conn, master_username, master_password):
    if master_username is None or master_password is None:
        raise ValueError("master_username and master_password cannot be None")
    try:
        salt = bcrypt.gensalt()
        hashed_master_password = bcrypt.hashpw(master_password.encode(), salt)
        cursor.execute("INSERT INTO users (master_username, hashed_password) VALUES (?, ?)", 
                    (master_username, hashed_master_password))
        conn.commit()
        print("User created successfully!")
    except sqlite3.IntegrityError:
        print("master_username already exists.")
    except (sqlite3.Error, Exception) as e:
        print(f"An error occurred: {e}")

# Authenticate the user
def authenticate_user(cursor, master_username, master_password):
    # Check for None values in input
    if not all([master_username, master_password]):
        raise AttributeError("master_username and master_password cannot be None")

    try:
        # Execute query to fetch hashed password
        cursor.execute("SELECT hashed_password FROM users WHERE master_username = ?", (master_username,))
        result = cursor.fetchone()
        # Check if user exists and password matches
        #result[0] is stored_hashed_password 
        if result and bcrypt.checkpw(master_password.encode(), result[0]):
            print("Authentication successful!")
            return True
        print("Incorrect password." if result else "master_username not found.")
    except (sqlite3.Error, Exception) as e:
        print(f"An error occurred: {e}")
    
    return False
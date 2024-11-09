from argon2 import PasswordHasher
import sqlite3

# Initialize the argon2 password hasher
ph = PasswordHasher()

def create_user(cursor, conn, master_username, master_password=None, check_only=False):
    if master_username is None:
        print("Error: Username cannot be empty.")
        return False

    # Check-only mode: Check for username existence without modifying the database
    if check_only:
        cursor.execute("SELECT 1 FROM users WHERE master_username = ?", (master_username,))
        return cursor.fetchone() is None  # Returns True if username does not exist

    try:
        hashed_master_password = ph.hash(master_password) 
        with conn:  # Context manager handles commit and rollback
            cursor.execute("INSERT INTO users (master_username, hashed_password) VALUES (?, ?)", 
                        (master_username, hashed_master_password))
        return True
    except sqlite3.IntegrityError:
        print("The username is unavailable. Please choose a different username.")
        return False
    except (sqlite3.Error, Exception) as e:
        print("An unexpected error occurred. Please try again.")
        return False

def authenticate_user(cursor, master_username, master_password):
    if master_username is None or master_password is None:
        print("Login failed: Username and password cannot be empty.")
        return False
    try:
        cursor.execute("SELECT hashed_password FROM users WHERE master_username = ?", (master_username,))
        result = cursor.fetchone()
        if result:
            try:
                # Verify the provided password with the stored hash
                # result[0] is stored_hashed_password
                if ph.verify(result[0], master_password):
                    input("Authentication successful.")
                    return True
            except:
                input("Error: Invalid master password.")
                return False
        else:
            input("Error: Master username does not exist.")
            return False
    except (sqlite3.Error, Exception) as e:
        input(f"An error occurred: {e}")
        return False
    return False
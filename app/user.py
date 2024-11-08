from argon2 import PasswordHasher
import sqlite3

# Initialize the argon2 password hasher
ph = PasswordHasher()

# Create a new user (master username and hashed master password)
def create_user(cursor, conn, master_username, master_password):
    if master_username is None or master_password is None:
        raise ValueError("master_username and master_password cannot be None")
    try:
        # Hash the master password with Argon2
        hashed_master_password = ph.hash(master_password)
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
        if result:
            # result[0] is stored_hashed_password
            try:
                # Verify the provided password with the stored hash
                if ph.verify(result[0], master_password):
                    print("Authentication successful!")
                    return True
            except:
                print("Incorrect password.")
        else:
            print("master_username not found.")
    except (sqlite3.Error, Exception) as e:
        print(f"An error occurred: {e}")
    return False
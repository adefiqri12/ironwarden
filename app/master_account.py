from argon2 import PasswordHasher
import sqlite3
import getpass
import os 
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.guideline import guideline, is_valid_username, is_strong_password, load_common_credentials

# Initialize the argon2 password hasher
ph = PasswordHasher()

def init_master_account(cursor, conn, master_username, master_password=None, check_only=False):
    if master_username is None:
        print("Error: Username cannot be empty.")
        return False
    # Check-only mode: Check for username existence without modifying the database
    if check_only:
        cursor.execute("SELECT 1 FROM master_accounts WHERE master_username = ?", (master_username,))
        return cursor.fetchone() is None  # Returns True if username does not exist
    try:
        hashed_master_password = ph.hash(master_password) 
        with conn:  # Context manager handles commit and rollback
            cursor.execute("INSERT INTO master_accounts (master_username, master_password) VALUES (?, ?)", 
                        (master_username, hashed_master_password))
        return True
    except sqlite3.IntegrityError:
        print("The username is unavailable. Please choose a different username.")
        return False
    except (sqlite3.Error, Exception) as e:
        print("An unexpected error occurred. Please try again.")
        return False

def auth_master_account(cursor, master_username, master_password):
    if master_username is None or master_password is None:
        print("Login failed: Username and password cannot be empty.")
        return False
    try:
        cursor.execute("SELECT master_password FROM master_accounts WHERE master_username = ?", (master_username,))
        result = cursor.fetchone()
        if result:
            try:
                # Verify the provided password with the stored hash
                # result[0] is stored_master_password
                if ph.verify(result[0], master_password):
                    print("Authentication successful.")
                    return True
            except:
                print("Error: Invalid master password.")
                return False
        else:
            print("Error: Master username does not exist.")
            return False
    except (sqlite3.Error, Exception) as e:
        print(f"An error occurred: {e}")
        return False
    return False


def create_master_account(conn, cursor):
    guideline()
    common_usernames = load_common_credentials("username")
    common_passwords = load_common_credentials("password") 
    # Loop until a valid and unique username is provided
    while True:
        new_master_username = input("Enter your new master username: ")
        if is_valid_username(new_master_username, common_usernames):
            # Attempt to create the user immediately to check for duplicates
            if init_master_account(cursor, conn, new_master_username, check_only=True):
                print("Username is available.")
                break  # Username is valid and unique
            else:
                print("Username already exists. Please try a different username.")
    # Now ask for the password
    while True:
        new_master_password = getpass.getpass("Enter your new master password: ")
        if is_strong_password(new_master_password, common_passwords):
            confirm_password = getpass.getpass("Confirm your new master password: ")
            if new_master_password == confirm_password:
                # Finalize account creation with the validated password
                init_master_account(cursor, conn, new_master_username, new_master_password)
                print("Account created successfully.")
                break
            else:
                print("Error: Passwords do not match. Please try again.")
        else:
            print("Password does not meet strength requirements. Please try again.\n")

def delete_master_account(conn, cursor):
    master_username = input("Enter the username of the account to delete: ")
    account = find_master_account(cursor, master_username)
    if account is None:
        print("Error: Username does not exist.")
        return
    master_password = getpass.getpass("Enter the password for this account to confirm deletion: ")
    if not auth_master_account(cursor, master_username, master_password):
        return
    confirmation = input(f"Are you sure you want to delete the account '{master_username}'? This action is irreversible (yes/no): ")
    if confirmation.lower() == 'yes':
        if db_delete_master_account(conn, cursor, master_username):
            print(f"Account '{master_username}' has been successfully deleted.")
    else:
        print("Account deletion canceled.")

def db_delete_master_account(conn, cursor, master_username):
    try:
        with conn:
            cursor.execute("DELETE FROM master_accounts WHERE master_username = ?", (master_username,))
        return True
    except sqlite3.Error as e:
        print(f"Error deleting account: {e}")
        return False
    
def find_master_account(cursor, master_username):
    """Check if a user exists in the database."""
    cursor.execute("SELECT * FROM master_accounts WHERE master_username = ?", (master_username,))
    return cursor.fetchone()
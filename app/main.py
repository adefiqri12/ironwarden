import sys
import pyperclip
import os
import getpass 
import ctypes
import sqlite3

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import init_db
from app.user import create_user, authenticate_user
from app.encryption import store_encrypted_password, update_encrypted_password, retrieve_encrypted_password
from app.guideline import print_ascii_welcome, guideline, is_valid_username, is_strong_password, load_common_credentials
from generator.password_generator import password_generator

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def secure_clear(data):
    """Securely clear data from memory."""
    if data is None or data == "":
        return None
    if isinstance(data, bytearray):
        ctypes.memset(ctypes.addressof(ctypes.c_char.from_buffer(data)), 0, len(data))
    elif isinstance(data, str):
        data_bytes = bytearray(data.encode())
        ctypes.memset(ctypes.addressof(ctypes.c_char.from_buffer(data_bytes)), 0, len(data_bytes))
    return None

def exit_program(conn, *args):
    """Clears sensitive data, closes the database connection, clears the screen, and exits the program."""
    for arg in args:
        if arg is not None:  # Only clear if the variable is not None
            arg = secure_clear(arg)
    if conn:
        conn.close()
    clear_screen()
    sys.exit()

def display_menu():
    clear_screen()
    print_ascii_welcome()
    print("1. Login")
    print("2. Create a New Master Account")
    print("3. Delete an Existing Master Account")
    print("4. Exit")

def main():
    conn, cursor = init_db()
    if conn is None or cursor is None:
        print("Error: Failed to initialize database. Exiting.")
        return
    
    master_username = None
    master_password = None

    while True:
        display_menu()
        choice = input("Enter your choice: ")
        if choice == '1':
            handle_login(conn, cursor, master_username, master_password)
        elif choice == '2':
            create_new_master_account(conn, cursor)
        elif choice == '3':
            delete_master_account(conn, cursor)
        elif choice == '4':
            exit_program(conn, master_username, master_password)
        else:
            print("Error: Please select a valid option.")

def handle_login(conn, cursor, master_username, master_password):
    master_username = input("Enter your username: ")
    account = find_master_account(cursor, master_username)
    if account is None:
        input("Error: Username does not exist.")
        return
    master_password = getpass.getpass("Enter your master password: ")

    if authenticate_user(cursor, master_username, master_password):
        print(f"\nWelcome, {master_username}!")
        handle_password_operations(conn, cursor, master_username, master_password)

def handle_password_operations(conn, cursor, master_username, master_password):
    while True:
        print("1. Store a new password")
        print("2. Retrieve a password")
        print("3. Delete a stored password")
        print("4. Update a stored password")
        print("5. Logout")
        option = input("Choose an option: ")
        if option == '1':
            store_password(conn, cursor, master_username, master_password)
        elif option == '2':
            retrieve_password(cursor, master_username, master_password)
        elif option == '3':
            delete_password(conn, cursor, master_username)
        elif option == '4':
            update_password(conn, cursor, master_username, master_password)
        elif option == '5':
            exit_program(conn, master_username, master_password)
        else:
            print("Error: Please select a valid option.")

def create_new_master_account(conn, cursor):
    guideline()
    common_usernames = load_common_credentials("username")
    common_passwords = load_common_credentials("password") 
    # Loop until a valid and unique username is provided
    while True:
        new_master_username = input("Enter your new master username: ")
        if is_valid_username(new_master_username, common_usernames):
            # Attempt to create the user immediately to check for duplicates
            if create_user(cursor, conn, new_master_username, check_only=True):
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
                create_user(cursor, conn, new_master_username, new_master_password)
                input("Account created successfully.")
                break
            else:
                print("Error: Passwords do not match. Please try again.")
        else:
            print("Password does not meet strength requirements. Please try again.\n")

def delete_master_account(conn, cursor):
    master_username = input("Enter the username of the account to delete: ")
    account = find_master_account(cursor, master_username)
    if account is None:
        input("Error: Username does not exist.")
        return
    master_password = getpass.getpass("Enter the password for this account to confirm deletion: ")
    if not authenticate_user(cursor, master_username, master_password):
        return
    confirmation = input(f"Are you sure you want to delete the account '{master_username}'? This action is irreversible (yes/no): ")
    if confirmation.lower() == 'yes':
        if db_delete_master_account(conn, cursor, master_username):
            input(f"Account '{master_username}' has been successfully deleted.")
    else:
        input("Account deletion canceled.")

def db_delete_master_account(conn, cursor, master_username):
    try:
        cursor.execute("DELETE FROM users WHERE master_username = ?", (master_username,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error deleting account: {e}")
        return False

def store_password(conn, cursor, master_username, master_password):
    site_name = input("Enter new account name or ID: ")
    use_generated_password = input("Do you want to generate a password? (y/n): ").strip().lower()

    if use_generated_password == 'y':
        password_to_store = password_generator()
        print(f"Generated Password: {password_to_store}")
    else:
        password_to_store = input("Enter the password to store: ")
    store_encrypted_password(cursor, conn, master_username, site_name, password_to_store, master_password)
    print(f"Password for '{site_name}' stored successfully.")

def retrieve_password(cursor, master_username, master_password):
    sites = get_stored_sites(cursor, master_username)
    if sites:
        display_sites(sites)
        choice = get_user_choice(len(sites))
        if choice is not None:
            selected_site = sites[choice][0]
            retrieved_password = retrieve_encrypted_password(cursor, master_username, selected_site, master_password)
            if retrieved_password:
                pyperclip.copy(retrieved_password)
                print(f"Password for '{selected_site}' has been copied to your clipboard.")
            else:
                print("Failed to retrieve password.")
    else:
        print("Error: No stored passwords found.")

def delete_password(conn, cursor, master_username):
    sites = get_stored_sites(cursor, master_username)
    if sites:
        display_sites(sites)
        choice = get_user_choice(len(sites))
        if choice is not None:
            selected_site = sites[choice][0]
            cursor.execute("DELETE FROM stored_passwords WHERE username = ? AND site_name = ?", 
                        (master_username, selected_site))
            conn.commit()
            print(f"Account '{selected_site}' has been deleted successfully.")
    else:
        print("Error: No stored passwords to delete.")

def update_password(conn, cursor, master_username, master_password):
    sites = get_stored_sites(cursor, master_username)
    if sites:
        display_sites(sites)
        choice = get_user_choice(len(sites))
        if choice is not None:
            selected_site = sites[choice][0]
            use_generated_password = input("Do you want to generate a password? (y/n): ").strip().lower()
            if use_generated_password == 'y':
                new_password = password_generator()
                print(f"Generated Password for'{selected_site}': {new_password}")
            else:
                new_password = input(f"Enter the new password for '{selected_site}': ")
            update_encrypted_password(cursor, conn, master_username, selected_site, new_password, master_password)
            pyperclip.copy(new_password)
            print(f"Password for '{selected_site}' has been updated successfully and copied.")
    else:
        print("Error: No stored passwords found.")

# Helper function to display stored sites
def display_sites(sites):
    print("\nStored Account/ID:")
    for idx, site in enumerate(sites, start=1):
        print(f"{idx}. {site[0]}")

# Helper function to get user's numeric choice for sites
def get_user_choice(site_count):
    try:
        choice = int(input("Select a number: ")) - 1
        if 0 <= choice < site_count:
            return choice
        else:
            print("Invalid selection.")
            return None
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None

# Helper function to get stored sites
def get_stored_sites(cursor, master_username):
    cursor.execute("SELECT site_name FROM stored_passwords WHERE username = ?", (master_username,))
    return cursor.fetchall()

def find_master_account(cursor, master_username):
    """Check if a user exists in the database."""
    cursor.execute("SELECT * FROM users WHERE master_username = ?", (master_username,))
    return cursor.fetchone()

if __name__ == "__main__":
    main()
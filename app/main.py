import time
import sys
import pyperclip
import os
import getpass 
import ctypes

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import init_db
from app.user import create_user, authenticate_user
from app.encryption import store_encrypted_password, update_encrypted_password, retrieve_encrypted_password
from app.ascii import print_ascii_welcome
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
    # Clear sensitive data
    for arg in args:
        if arg is not None:  # Only clear if the variable is not None
            arg = secure_clear(arg)
    # Close database connection if open
    if conn:
        conn.close()
    clear_screen()
    sys.exit()

def main():
    conn, cursor = init_db()
    if conn is None or cursor is None:
        print("Failed to initialize database. Exiting.")
        return

    clear_screen()
    print_ascii_welcome()

    login_username = None
    login_password = None

    while True:
        print("1. Login")
        print("2. Create a New Account")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            handle_login(conn, cursor, login_username, login_password)
        elif choice == '2':
            create_new_account(conn, cursor)
        elif choice == '3':
            exit_program(conn, login_username, login_password)
        else:
            print("Invalid choice. Please choose again.")

def handle_login(conn, cursor, login_username, login_password):
    login_username = input("Enter your username: ")
    login_password = getpass.getpass("Enter your master password: ")

    if authenticate_user(cursor, login_username, login_password):
        print(f"Welcome, {login_username}!")
        handle_password_operations(conn, cursor, login_username, login_password)
    else:
        print("Login failed. Please try again.")

def handle_password_operations(conn, cursor, login_username, login_password):
    while True:
        print("\nOptions:")
        print("1. Store a new password")
        print("2. Retrieve a password")
        print("3. Delete a stored password")
        print("4. Update a stored password")
        print("5. Logout")
        option = input("Choose an option: ")
        if option == '1':
            store_password(conn, cursor, login_username, login_password)
        elif option == '2':
            retrieve_password(cursor, login_username, login_password)
        elif option == '3':
            delete_password(conn, cursor, login_username)
        elif option == '4':
            update_password(conn, cursor, login_username, login_password)
        elif option == '5':
            exit_program(conn, login_username, login_password)
        else:
            print("Invalid option. Please choose again.")

def create_new_account(conn, cursor):
    new_master_username = input("Enter your new master username: ")
    new_master_password = getpass.getpass("Enter your new master password: ")
    confirm_password = getpass.getpass("Confirm your new master password: ")
    
    if new_master_password == confirm_password:
        create_user(cursor, conn, new_master_username, new_master_password)
    else:
        print("Passwords do not match. Please try again.")

def store_password(conn, cursor, login_username, login_password):
    site_name = input("Enter new account name or ID: ")
    use_generated_password = input("Do you want to generate a password? (y/n): ").strip().lower()

    if use_generated_password == 'y':
        password_to_store = password_generator()
        print(f"Generated Password: {password_to_store}")
    else:
        password_to_store = input("Enter the password to store: ")
    start_time = time.time()
    store_encrypted_password(cursor, conn, login_username, site_name, password_to_store, login_password)
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f} seconds")

def retrieve_password(cursor, login_username, login_password):
    sites = get_stored_sites(cursor, login_username)
    if sites:
        display_sites(sites)
        choice = get_user_choice(len(sites))
        if choice is not None:
            selected_site = sites[choice][0]
            retrieved_password = retrieve_encrypted_password(cursor, login_username, selected_site, login_password)
            if retrieved_password:
                pyperclip.copy(retrieved_password)
                print(f"Password for '{selected_site}' has been copied to your clipboard.")
            else:
                print("Failed to retrieve password.")
    else:
        print("No stored passwords found.")

def delete_password(conn, cursor, login_username):
    sites = get_stored_sites(cursor, login_username)
    if sites:
        display_sites(sites)
        choice = get_user_choice(len(sites))
        if choice is not None:
            selected_site = sites[choice][0]
            cursor.execute("DELETE FROM stored_passwords WHERE username = ? AND site_name = ?", 
                        (login_username, selected_site))
            conn.commit()
            print(f"Account '{selected_site}' has been deleted successfully.")
    else:
        print("No stored passwords to delete.")

def update_password(conn, cursor, login_username, login_password):
    sites = get_stored_sites(cursor, login_username)
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
            update_encrypted_password(cursor, conn, login_username, selected_site, new_password, login_password)
            print(f"Password for '{selected_site}' has been updated successfully.")
    else:
        print("No stored passwords found.")

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
def get_stored_sites(cursor, login_username):
    cursor.execute("SELECT site_name FROM stored_passwords WHERE username = ?", (login_username,))
    return cursor.fetchall()

if __name__ == "__main__":
    main()
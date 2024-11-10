import sys
import os
import getpass 
import ctypes

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import init_db
from app.master_account import auth_master_account, create_master_account, delete_master_account, find_master_account
from app.guideline import print_ascii_welcome
from app.data_management import store_password, retrieve_password, update_password, delete_password 

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
            create_master_account(conn, cursor)
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

    if auth_master_account(cursor, master_username, master_password):
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

if __name__ == "__main__":
    main()
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

def clear_screen():
    # Check the operating system and clear accordingly
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For macOS and Linux
        os.system('clear')

import ctypes

def secure_clear(data):
    """
    Securely clear sensitive data from memory.

    This function attempts to overwrite the contents of the provided data
    with zeros to reduce the risk of sensitive information being left in
    memory. It handles both bytearrays and strings, converting strings into
    bytearrays before clearing. After clearing the content, it returns None
    to remove references to the data.

    Args:
        data (str or bytearray): The sensitive data to be cleared from memory.

    Returns:
        None
    """
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
    
    login_username = None
    login_password = None
    retrieved_password = None
    sites = None

    clear_screen()
    print_ascii_welcome()    
    while True:
        print("1. Login")
        print("2. Create a New Account")
        print("3. Exit")
        choice = input("Enter your choice: ")
    
        if choice == '1':
            # User Login
            login_username = input("Enter your username: ")
            login_password = getpass.getpass("Enter your master password: ")
            
            if authenticate_user(cursor, login_username, login_password):
                # Authenticated session for this user
                print(f"Welcome, {login_username}!")
                
                while True:
                    print("\nOptions:")
                    print("1. Store a new password")
                    print("2. Retrieve a password")
                    print("3. Delete a stored password")
                    print("4. Update a stored password")
                    print("5. Logout")
                    option = input("Choose an option: ")
                    
                    if option == '1':
                        # Store a new password
                        site_name = input("Enter new account name or ID: ")
                        password_to_store = input("Enter the password to store: ")
                        start_time = time.time()
                        store_encrypted_password(cursor, conn, login_username, site_name, password_to_store, login_password)
                        end_time = time.time()
                        execution_time = end_time - start_time
                        print(f"Execution time: {execution_time:.2f} seconds")
                    
                    elif option == '2':
                        # Retrieve stored password
                        cursor.execute("SELECT site_name FROM stored_passwords WHERE username = ?", (login_username,))
                        sites = cursor.fetchall()
                        if sites:
                            print("\nStored Account/ID:")
                            for idx, site in enumerate(sites, start=1):
                                print(f"{idx}. {site[0]}")
                            
                            try:
                                choice = int(input("Select a number to view the password: ")) - 1
                                if 0 <= choice < len(sites):
                                    selected_site = sites[choice][0]
                                    retrieved_password = retrieve_encrypted_password(cursor, login_username, selected_site, login_password)
                                    if retrieved_password:
                                        pyperclip.copy(retrieved_password)
                                        print(f"Password for '{selected_site}' has been copied to your clipboard.")
                                    else:
                                        print("Failed to retrieve password.")
                                else:
                                    print("Invalid selection.")
                            except ValueError:
                                print("Invalid input. Please enter a number.")
                        else:
                            print("No stored passwords found.")
                    elif option == '3':
                        # Delete a stored account and password
                        cursor.execute("SELECT site_name FROM stored_passwords WHERE username = ?", (login_username,))
                        sites = cursor.fetchall()
                        if sites:
                            print("\nStored Account/ID:")
                            for idx, site in enumerate(sites, start=1):
                                print(f"{idx}. {site[0]}")
                            try:
                                choice = int(input("Select a number to delete the account: ")) - 1
                                if 0 <= choice < len(sites):
                                    selected_site = sites[choice][0]
                                    # Perform deletion from the database
                                    cursor.execute("DELETE FROM stored_passwords WHERE username = ? AND site_name = ?", 
                                                (login_username, selected_site))
                                    conn.commit()
                                    print(f"Account '{selected_site}' has been deleted successfully.")
                                else:
                                    print("Invalid selection.")
                            except ValueError:
                                print("Invalid input. Please enter a number.")
                        else:
                            print("No stored passwords to delete.")
                    elif option == '4':
                        # Update stored password
                        cursor.execute("SELECT site_name FROM stored_passwords WHERE username = ?", (login_username,))
                        sites = cursor.fetchall()
                        if sites:
                            print("\nStored Account/ID:")
                            for idx, site in enumerate(sites, start=1):
                                print(f"{idx}. {site[0]}")
                            
                            try:
                                choice = int(input("Select a number to update the password: ")) - 1
                                if 0 <= choice < len(sites):
                                    selected_site = sites[choice][0]
                                    new_password = input(f"Enter the new password for '{selected_site}': ")
                                    update_encrypted_password(cursor, conn, login_username, selected_site, new_password, login_password)
                                    print(f"Password for '{selected_site}' has been updated successfully.")
                                else:
                                    print("Invalid selection.")
                            except ValueError:
                                print("Invalid input. Please enter a number.")
                        else:
                            print("No stored passwords found.")
                    
                    elif option == '5':
                        exit_program(conn, login_username, login_password, retrieved_password, sites)
                    else:
                        print("Invalid option. Please choose again.")
            else:
                print("Login failed. Please try again.")
        elif choice == '2':
            new_master_username = input("Enter your new master username: ")
            new_master_password = getpass.getpass("Enter your new master password: ")
            confirm_password = getpass.getpass("Confirm your new master password: ")
            if new_master_password != confirm_password:
                print("Passwords do not match. Please try again.")
            else:
                create_user(cursor, conn, new_master_username, new_master_password)
        elif choice == '3':
            exit_program(conn, login_username, login_password, retrieved_password, sites)
        else:
            print("Invalid choice. Please choose again.")

if __name__ == "__main__":
    main()
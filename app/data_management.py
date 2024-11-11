import pyperclip
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.encryption import store_encrypted_password, update_encrypted_password, retrieve_encrypted_password
from generator.password_generator import password_generator

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
    username = retrieve_stored_username(cursor, master_username)
    if username:
        display_stored_username(username)
        choice = get_user_choice(len(username))
        if choice is not None:
            selected_site = username[choice][0]
            retrieved_password = retrieve_encrypted_password(cursor, master_username, selected_site, master_password)
            if retrieved_password:
                pyperclip.copy(retrieved_password)
                print(f"Password for '{selected_site}' has been copied to your clipboard.")
            else:
                print("Failed to retrieve password.")
    else:
        print("Error: No stored passwords found.")

def delete_password(conn, cursor, master_username):
    username = retrieve_stored_username(cursor, master_username)
    if username:
        display_stored_username(username)
        choice = get_user_choice(len(username))
        if choice is not None:
            selected_site = username[choice][0]
            cursor.execute("DELETE FROM data_vault WHERE username = ? AND site_name = ?", 
                        (master_username, selected_site))
            conn.commit()
            print(f"Account '{selected_site}' has been deleted successfully.")
    else:
        print("Error: No stored passwords to delete.")

def update_password(conn, cursor, master_username, master_password):
    username = retrieve_stored_username(cursor, master_username)
    if username:
        display_stored_username(username)
        choice = get_user_choice(len(username))
        if choice is not None:
            selected_site = username[choice][0]
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

# Helper function to display stored username
def display_stored_username(username):
    print("\nStored Account/ID:")
    for idx, site in enumerate(username, start=1):
        print(f"{idx}. {site[0]}")

# Helper function to get user's numeric choice for username
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

# Helper function to get stored username
def retrieve_stored_username(cursor, master_username):
    cursor.execute("SELECT site_name FROM data_vault WHERE username = ?", (master_username,))
    return cursor.fetchall()
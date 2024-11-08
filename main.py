from database import init_db
from user import create_user, authenticate_user
from encryption import store_encrypted_password, retrieve_encrypted_password
import time

def main():

    conn, cursor = init_db()
    if conn is None or cursor is None:
        print("Failed to initialize database. Exiting.")
        return
    print("WELCOME TO THE PASSWORD MANAGER")

    while True:
        print("\nChoose an option:")
        print("1. Login")
        print("2. Create a New Account")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            # User Login
            login_username = input("Enter your username: ")
            login_password = input("Enter your master password: ")
            
            if authenticate_user(cursor, login_username, login_password):
                # Authenticated session for this user
                print(f"Welcome, {login_username}!")
                
                while True:
                    print("\nOptions:")
                    print("1. Store a new password")
                    print("2. Retrieve a password")
                    print("3. Logout")
                    option = input("Choose an option: ")
                    
                    if option == '1':
                        # Store a new password
                        site_name = input("Enter the site name or ID: ")
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
                            print("\nStored Sites:")
                            for idx, site in enumerate(sites, start=1):
                                print(f"{idx}. {site[0]}")
                            
                            try:
                                choice = int(input("Select a site number to view the password: ")) - 1
                                if 0 <= choice < len(sites):
                                    selected_site = sites[choice][0]
                                    retrieved_password = retrieve_encrypted_password(cursor, login_username, selected_site, login_password)
                                    if retrieved_password:
                                        print(f"Password for '{selected_site}': {retrieved_password}")
                                    else:
                                        print("Failed to retrieve password.")
                                else:
                                    print("Invalid selection.")
                            except ValueError:
                                print("Invalid input. Please enter a number.")
                        else:
                            print("No stored passwords found.")
                    
                    elif option == '3':
                        # Logout
                        print(f"Logging out {login_username}...")
                        break
                    else:
                        print("Invalid option. Please choose again.")
            else:
                print("Login failed. Please try again.")
        
        elif choice == '2':
            # Create New User
            new_master_username = input("Enter your new master username: ")
            new_master_password = input("Enter your new master password: ")
            create_user(cursor, conn, new_master_username, new_master_password)
        
        elif choice == '3':
            # Exit the program
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please choose again.")

    # Close the database connection when done
    conn.close()

if __name__ == "__main__":
    main()
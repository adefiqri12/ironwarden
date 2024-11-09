import getpass

def simple_password_manager():
    conn, cursor = init_db()
    if conn is None or cursor is None:
        print("Database initialization failed.")
        return

    while True:
        print("\nMain Menu:")
        print("1. Login")
        print("2. Create Account")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            username = input("Username: ")
            master_password = getpass.getpass("Password: ")
            
            if authenticate_user(cursor, username, master_password):
                print(f"\nWelcome, {username}!")
                
                while True:
                    print("\n1. Store Password")
                    print("2. Retrieve Password")
                    print("3. Delete Password")
                    print("4. Update Password")
                    print("5. Logout")
                    auth_choice = input("Choose an action: ")

                    if auth_choice == '1':
                        # Store Password
                        site = input("Site Name: ")
                        site_password = input("Password: ")
                        store_encrypted_password(cursor, conn, username, site, site_password, master_password)
                        print("Password stored.")

                    elif auth_choice == '2':
                        # Retrieve Password
                        cursor.execute("SELECT site_name FROM stored_passwords WHERE username = ?", (username,))
                        sites = [site[0] for site in cursor.fetchall()]
                        
                        for idx, site in enumerate(sites, start=1):
                            print(f"{idx}. {site}")
                        
                        if sites:
                            site_idx = int(input("Select site number: ")) - 1
                            site_name = sites[site_idx]
                            password = retrieve_encrypted_password(cursor, username, site_name, master_password)
                            print(f"Password for {site_name}: {password}")

                    elif auth_choice == '3':
                        # Delete Password
                        cursor.execute("SELECT site_name FROM stored_passwords WHERE username = ?", (username,))
                        sites = [site[0] for site in cursor.fetchall()]
                        
                        for idx, site in enumerate(sites, start=1):
                            print(f"{idx}. {site}")
                        
                        if sites:
                            site_idx = int(input("Select site number to delete: ")) - 1
                            cursor.execute("DELETE FROM stored_passwords WHERE username = ? AND site_name = ?", (username, sites[site_idx]))
                            conn.commit()
                            print("Password deleted.")

                    elif auth_choice == '4':
                        # Update Password
                        cursor.execute("SELECT site_name FROM stored_passwords WHERE username = ?", (username,))
                        sites = [site[0] for site in cursor.fetchall()]
                        
                        for idx, site in enumerate(sites, start=1):
                            print(f"{idx}. {site}")
                        
                        if sites:
                            site_idx = int(input("Select site number to update: ")) - 1
                            new_password = input(f"New password for {sites[site_idx]}: ")
                            update_encrypted_password(cursor, conn, username, sites[site_idx], new_password, master_password)
                            print("Password updated.")

                    elif auth_choice == '5':
                        print("Logging out.")
                        break
            else:
                print("Authentication failed.")

        elif choice == '2':
            # Account Creation
            username = input("New Username: ")
            password = getpass.getpass("New Password: ")
            confirm_password = getpass.getpass("Confirm Password: ")

            if password == confirm_password:
                create_user(cursor, conn, username, password)
                print("Account created.")
            else:
                print("Passwords do not match.")

        elif choice == '3':
            print("Goodbye!")
            conn.close()
            break

if __name__ == "__main__":
    simple_password_manager()
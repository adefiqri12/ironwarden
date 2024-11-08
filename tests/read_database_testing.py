import sqlite3
import os

# Path to your SQLite database file
db_path = 'password_manager.db'

# Check if the database exists
db_exists = os.path.exists(db_path)

# Connect to the SQLite database (it will create it if it doesn't exist)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create the tables if they don't already exist
if not db_exists:
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        master_username TEXT PRIMARY KEY,
        hashed_password BLOB
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stored_passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        site_name TEXT,
        salt BLOB,
        iv BLOB,
        encrypted_password BLOB,
        FOREIGN KEY (username) REFERENCES users(master_username)
    )
    ''')
    conn.commit()  # Commit changes if tables were created

# Function to fetch and print all records from a table
def fetch_all(table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    print(f"\nData from {table_name}:")
    for row in rows:
        print(row)

# Query and print data from the 'users' table
fetch_all('users')

# Query and print data from the 'stored_passwords' table
fetch_all('stored_passwords')

# Close the connection
conn.close()
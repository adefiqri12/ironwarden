import sqlite3
import os

# Path to your SQLite database file
db_path = 'db.sqlite3'

# Check if the database exists
db_exists = os.path.exists(db_path)

# Connect to the SQLite database (it will create it if it doesn't exist)
conn = sqlite3.connect(db_path)
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

# Create the tables if they don't already exist
if not db_exists:
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS master_accounts (
        master_username TEXT PRIMARY KEY,
        master_password BLOB
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS data_vault (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        site_name TEXT,
        salt BLOB,
        iv BLOB,
        encrypted_password BLOB,
        FOREIGN KEY (username) REFERENCES master_accounts(master_username)
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

# Query and print data from the 'master_accounts' table
fetch_all('master_accounts')

# Query and print data from the 'data_vault' table
fetch_all('data_vault')

# Close the connection
conn.close()
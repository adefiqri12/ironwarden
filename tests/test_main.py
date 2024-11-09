import unittest
from unittest.mock import Mock, patch, MagicMock
import sqlite3
import os
import pyperclip
from io import StringIO
import sys

# Import the functions to test
from app.main import (
    secure_clear,
    handle_login,
    store_password,
    retrieve_password,
    delete_password,
    update_password,
    get_stored_sites,
    create_new_account
)

class TestPasswordManager(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a test database connection
        self.conn = sqlite3.connect(':memory:')
        # Enable foreign key support
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor()
        
        # Create necessary tables with correct schema
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                master_username TEXT PRIMARY KEY,
                hashed_password BLOB
            )
        ''')
        
        self.cursor.execute('''
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
        
        # Test user credentials
        self.test_username = "testuser"
        self.test_password = "testpass123"
        
        # Insert test user with mock hashed password
        self.cursor.execute(
            "INSERT INTO users (master_username, hashed_password) VALUES (?, ?)",
            (self.test_username, b"dummy_hashed_password")
        )
        self.conn.commit()
        
    def tearDown(self):
        """Clean up after each test method."""
        self.conn.close()
        
    def test_secure_clear(self):
        """Test secure clearing of sensitive data."""
        # Test with string
        test_string = "sensitive_data"
        result = secure_clear(test_string)
        self.assertIsNone(result)
        
        # Test with bytearray
        test_bytearray = bytearray(b"sensitive_data")
        result = secure_clear(test_bytearray)
        self.assertIsNone(result)
        
        # Test with None
        result = secure_clear(None)
        self.assertIsNone(result)

    @patch('app.user.hash_password')
    @patch('getpass.getpass')
    @patch('builtins.input')
    def test_create_new_account(self, mock_input, mock_getpass, mock_hash):
        """Test account creation functionality."""
        # Mock user inputs
        mock_input.return_value = "newuser"
        mock_getpass.side_effect = ["newpass123", "newpass123"]
        
        # Mock password hashing
        mock_hash.return_value = b"dummy_hashed_password"
        
        # Test account creation
        create_new_account(self.conn, self.cursor)
        
        # Verify account was created
        self.cursor.execute("SELECT master_username FROM users WHERE master_username = ?", 
                        ("newuser",))
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "newuser")

    @patch('time.time', side_effect=[0, 1])  # Mock start and end times
    @patch('app.encryption.store_encrypted_password')
    def test_store_password(self, mock_store_encrypted, mock_time):
        """Test password storage functionality."""
        # Mock inputs
        site_name = "testsite"
        password = "sitepass123"
        
        # Mock the encryption function
        mock_store_encrypted.return_value = True
        
        with patch('builtins.input', side_effect=[site_name, password]):
            store_password(self.conn, self.cursor, self.test_username, self.test_password)
            
        # Verify store_encrypted_password was called with correct parameters
        mock_store_encrypted.assert_called_once_with(
            self.cursor,
            self.conn,
            self.test_username,
            site_name,
            password,
            self.test_password
        )

    def test_get_stored_sites(self):
        """Test retrieval of stored sites."""
        # Insert test data
        test_sites = [("site1",), ("site2",), ("site3",)]
        for site in test_sites:
            self.cursor.execute(
                """INSERT INTO stored_passwords 
                (username, site_name, salt, iv, encrypted_password) 
                VALUES (?, ?, ?, ?, ?)""",
                (self.test_username, site[0], b"dummy_salt", b"dummy_iv", b"dummy_encrypted_password")
            )
        self.conn.commit()
        
        # Test retrieval
        sites = get_stored_sites(self.cursor, self.test_username)
        self.assertEqual(len(sites), 3)
        self.assertEqual([site[0] for site in sites], ["site1", "site2", "site3"])

    @patch('app.encryption.retrieve_encrypted_password')
    @patch('pyperclip.copy')
    def test_retrieve_password(self, mock_copy, mock_retrieve):
        """Test password retrieval functionality."""
        # Setup test data
        test_site = "testsite"
        test_password = "retrievedpass123"
        
        # Mock the retrieval function
        mock_retrieve.return_value = test_password
        
        # Insert test site
        self.cursor.execute(
            """INSERT INTO stored_passwords 
            (username, site_name, salt, iv, encrypted_password) 
            VALUES (?, ?, ?, ?, ?)""",
            (self.test_username, test_site, b"dummy_salt", b"dummy_iv", b"dummy_encrypted_password")
        )
        self.conn.commit()
        
        # Mock input to select the first site
        with patch('builtins.input', return_value="1"):
            retrieve_password(self.cursor, self.test_username, self.test_password)
            
        # Verify password was copied to clipboard
        mock_copy.assert_called_once_with(test_password)

    def test_delete_password(self):
        """Test password deletion functionality."""
        # Insert test data
        test_site = "testsite"
        self.cursor.execute(
            """INSERT INTO stored_passwords 
            (username, site_name, salt, iv, encrypted_password) 
            VALUES (?, ?, ?, ?, ?)""",
            (self.test_username, test_site, b"dummy_salt", b"dummy_iv", b"dummy_encrypted_password")
        )
        self.conn.commit()
        
        # Mock input to select the first site
        with patch('builtins.input', return_value="1"):
            delete_password(self.conn, self.cursor, self.test_username)
        
        # Verify password was deleted
        self.cursor.execute(
            "SELECT * FROM stored_passwords WHERE username = ? AND site_name = ?",
            (self.test_username, test_site)
        )
        result = self.cursor.fetchone()
        self.assertIsNone(result)

    @patch('app.encryption.update_encrypted_password')
    def test_update_password(self, mock_update):
        """Test password update functionality."""
        # Setup test data
        test_site = "testsite"
        new_password = "newpass123"
        
        # Insert test site
        self.cursor.execute(
            """INSERT INTO stored_passwords 
            (username, site_name, salt, iv, encrypted_password) 
            VALUES (?, ?, ?, ?, ?)""",
            (self.test_username, test_site, b"dummy_salt", b"dummy_iv", b"dummy_encrypted_password")
        )
        self.conn.commit()
        
        # Mock the update function
        mock_update.return_value = True
        
        # Mock inputs
        with patch('builtins.input', side_effect=["1", new_password]):
            update_password(self.conn, self.cursor, self.test_username, self.test_password)
            
        # Verify update_encrypted_password was called with correct parameters
        mock_update.assert_called_once_with(
            self.cursor,
            self.conn,
            self.test_username,
            test_site,
            new_password,
            self.test_password
        )

if __name__ == '__main__':
    unittest.main()
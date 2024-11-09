import unittest
from unittest.mock import Mock, patch
import sqlite3
from argon2 import PasswordHasher
from app.master_account import init_master_account, auth_master_account
import sys, pathlib

# Add the parent directory to the Python path
sys.path.append(str(pathlib.Path(__file__).parent.parent))

class TestUser(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test."""
        self.cursor = Mock()
        self.conn = Mock()
        self.username = "testuser"
        self.password = "testpass123"
        self.ph = PasswordHasher()

    def test_init_master_account_success(self):
        """Test successful user creation."""
        init_master_account(self.cursor, self.conn, self.username, self.password)
        
        # Verify database interactions
        self.cursor.execute.assert_called_once()
        self.conn.commit.assert_called_once()
        
        # Verify the stored password is properly hashed
        call_args = self.cursor.execute.call_args[0]
        stored_hash = call_args[1][1]
        self.assertTrue(self.ph.verify(stored_hash, self.password))

    def test_init_master_account_duplicate(self):
        """Test handling of duplicate username."""
        self.cursor.execute.side_effect = sqlite3.IntegrityError("UNIQUE constraint failed")
        
        with patch('builtins.print') as mock_print:
            init_master_account(self.cursor, self.conn, self.username, self.password)
            mock_print.assert_called_with("master_username already exists.")

    def test_init_master_account_none_values(self):
        """Test handling of None values."""
        with self.assertRaises(ValueError):
            init_master_account(self.cursor, self.conn, None, self.password)
        
        with self.assertRaises(ValueError):
            init_master_account(self.cursor, self.conn, self.username, None)

    def test_init_master_account_database_error(self):
        """Test handling of database errors."""
        self.cursor.execute.side_effect = sqlite3.Error("Test database error")
        
        with patch('builtins.print') as mock_print:
            init_master_account(self.cursor, self.conn, self.username, self.password)
            mock_print.assert_called_with("An error occurred: Test database error")

    def test_auth_master_account_success(self):
        """Test successful user authentication."""
        # Create hashed password
        master_password = self.ph.hash(self.password)
        self.cursor.fetchone.return_value = (master_password,)
        
        result = auth_master_account(self.cursor, self.username, self.password)
        
        self.assertTrue(result)
        self.cursor.execute.assert_called_once_with(
            "SELECT master_password FROM master_accounts WHERE master_username = ?",
            (self.username,)
        )

    def test_auth_master_account_wrong_password(self):
        """Test authentication with wrong password."""
        master_password = self.ph.hash(self.password)
        self.cursor.fetchone.return_value = (master_password,)
        
        result = auth_master_account(self.cursor, self.username, "wrongpass")
        
        self.assertFalse(result)

    def test_auth_master_account_nonexistent(self):
        """Test authentication with non-existent username."""
        self.cursor.fetchone.return_value = None
        
        result = auth_master_account(self.cursor, self.username, self.password)
        
        self.assertFalse(result)

    def test_auth_master_account_none_values(self):
        """Test authentication with None values."""
        with self.assertRaises(AttributeError):
            auth_master_account(self.cursor, None, self.password)
        
        with self.assertRaises(AttributeError):
            auth_master_account(self.cursor, self.username, None)

    def test_auth_master_account_database_error(self):
        """Test handling of database errors during authentication."""
        self.cursor.execute.side_effect = sqlite3.Error("Test database error")
        
        result = auth_master_account(self.cursor, self.username, self.password)
        
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
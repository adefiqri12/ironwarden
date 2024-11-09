import unittest
from unittest.mock import Mock, patch
import os
import sqlite3
from app.database import init_db
import sys, pathlib

# Add the parent directory to the Python path
sys.path.append(str(pathlib.Path(__file__).parent.parent))

class TestDatabase(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test."""
        self.test_db = 'test_db.sqlite3'
        # Ensure test database doesn't exist before each test
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def tearDown(self):
        """Clean up after each test."""
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_init_db_new_database(self):
        """Test creating a new database with tables."""
        conn, cursor = init_db(self.test_db)
        
        try:
            # Verify database was created
            self.assertTrue(os.path.exists(self.test_db))
            
            # Verify tables were created
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            table_names = [table[0] for table in tables]
            
            self.assertIn('master_accounts', table_names)
            self.assertIn('data_vault', table_names)
            
            # Verify master_accounts table structure
            cursor.execute("PRAGMA table_info(master_accounts)")
            master_accounts_columns = {row[1]: row[2] for row in cursor.fetchall()}
            self.assertEqual(master_accounts_columns['master_username'], 'TEXT')
            self.assertEqual(master_accounts_columns['master_password'], 'BLOB')
            
            # Verify data_vault table structure
            cursor.execute("PRAGMA table_info(data_vault)")
            passwords_columns = {row[1]: row[2] for row in cursor.fetchall()}
            self.assertEqual(passwords_columns['id'], 'INTEGER')
            self.assertEqual(passwords_columns['username'], 'TEXT')
            self.assertEqual(passwords_columns['site_name'], 'TEXT')
            self.assertEqual(passwords_columns['salt'], 'BLOB')
            self.assertEqual(passwords_columns['iv'], 'BLOB')
            self.assertEqual(passwords_columns['encrypted_password'], 'BLOB')
        finally:
            if conn:
                conn.close()

    def test_init_db_existing_database(self):
        """Test connecting to an existing database."""
        # Create initial database
        conn1, cursor1 = init_db(self.test_db)
        conn1.close()
        
        # Connect to existing database
        with patch('builtins.print') as mock_print:
            conn2, cursor2 = init_db(self.test_db)
            
            try:
                mock_print.assert_called_with("Database already exists")
                self.assertIsNotNone(conn2)
                self.assertIsNotNone(cursor2)
            finally:
                if conn2:
                    conn2.close()

    def test_init_db_sqlite_error(self):
        """Test handling of SQLite errors during initialization."""
        with patch('sqlite3.connect') as mock_connect:
            mock_connect.side_effect = sqlite3.Error("Test SQLite error")
            conn, cursor = init_db(self.test_db)
            
            self.assertIsNone(conn)
            self.assertIsNone(cursor)

    def test_init_db_general_error(self):
        """Test handling of general errors during initialization."""
        with patch('sqlite3.connect') as mock_connect:
            mock_connect.side_effect = Exception("Test general error")
            conn, cursor = init_db(self.test_db)
            
            self.assertIsNone(conn)
            self.assertIsNone(cursor)

def test_database_foreign_key_constraint(self):
    """Test that foreign key constraints are properly set up."""
    conn, cursor = init_db(self.test_db)
    
    try:
        # First verify foreign keys are enabled
        cursor.execute("PRAGMA foreign_keys")
        self.assertEqual(cursor.fetchone()[0], 1)
        
        # Try to insert a password record with non-existent username
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute("""
                INSERT INTO data_vault (username, site_name, salt, iv, encrypted_password)
                VALUES (?, ?, ?, ?, ?)
            """, ('nonexistent_user', 'test.com', b'salt', b'iv', b'encrypted'))
            conn.commit()
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    unittest.main()
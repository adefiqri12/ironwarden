import unittest
from unittest.mock import Mock, patch
import os
import sys
import pathlib

# Add the parent directory to the Python path
sys.path.append(str(pathlib.Path(__file__).parent.parent))

from encryption import derive_key, store_encrypted_password, retrieve_encrypted_password
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class TestEncryption(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test."""
        self.cursor = Mock()
        self.conn = Mock()
        self.username = "testuser"
        self.site_name = "example.com"
        self.password = "testpassword123"
        self.master_password = "masterpass123"

    def test_derive_key(self):
        """Test key derivation function."""
        salt = os.urandom(16)
        
        # Test key derivation produces expected length
        key = derive_key(self.master_password, salt)
        self.assertEqual(len(key), 32)  # AES-256 key length
        
        # Test same inputs produce same key
        key2 = derive_key(self.master_password, salt)
        self.assertEqual(key, key2)
        
        # Test different salts produce different keys
        salt2 = os.urandom(16)
        key3 = derive_key(self.master_password, salt2)
        self.assertNotEqual(key, key3)

    def test_store_encrypted_password(self):
        """Test password encryption and storage."""
        # Store password
        store_encrypted_password(
            self.cursor,
            self.conn,
            self.username,
            self.site_name,
            self.password,
            self.master_password
        )
        
        # Verify database interactions
        self.cursor.execute.assert_called_once()
        self.conn.commit.assert_called_once()
        
        # Verify the stored data
        call_args = self.cursor.execute.call_args[0]
        query = call_args[0]
        params = call_args[1]
        
        self.assertIn("INSERT INTO stored_passwords", query)
        self.assertEqual(params[0], self.username)
        self.assertEqual(params[1], self.site_name)
        self.assertEqual(len(params[2]), 16)  # salt length
        self.assertEqual(len(params[3]), 16)  # iv length
        self.assertTrue(len(params[4]) > 0)   # encrypted password

    def test_retrieve_encrypted_password(self):
        """Test password retrieval and decryption."""
        # Mock stored encrypted password
        salt = os.urandom(16)
        key = derive_key(self.master_password, salt)
        iv = os.urandom(16)
        
        # Create real encryption for test
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        
        # Pad and encrypt test password
        from cryptography.hazmat.primitives import padding
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(self.password.encode()) + padder.finalize()
        encrypted_password = encryptor.update(padded_data) + encryptor.finalize()
        
        # Mock database return value
        self.cursor.fetchone.return_value = (salt, iv, encrypted_password)
        
        # Test password retrieval
        retrieved_password = retrieve_encrypted_password(
            self.cursor,
            self.username,
            self.site_name,
            self.master_password
        )
        
        self.assertEqual(retrieved_password, self.password)
        
        # Verify database query
        self.cursor.execute.assert_called_once_with(
            "SELECT salt, iv, encrypted_password FROM stored_passwords WHERE username = ? AND site_name = ?",
            (self.username, self.site_name)
        )

    def test_retrieve_nonexistent_password(self):
        """Test retrieval of non-existent password."""
        self.cursor.fetchone.return_value = None
        
        result = retrieve_encrypted_password(
            self.cursor,
            self.username,
            self.site_name,
            self.master_password
        )
        
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
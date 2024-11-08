import unittest
from unittest.mock import Mock, patch, call
from io import StringIO
import sys
from main import main
import pathlib 

# Add the parent directory to the Python path
sys.path.append(str(pathlib.Path(__file__).parent.parent))

class TestPasswordManager(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Mock database connection and cursor
        self.mock_conn = Mock()
        self.mock_cursor = Mock()
        
        # Mock database initialization
        self.init_db_patcher = patch('main.init_db')
        self.mock_init_db = self.init_db_patcher.start()
        self.mock_init_db.return_value = (self.mock_conn, self.mock_cursor)
        
        # Mock user-related functions
        self.create_user_patcher = patch('main.create_user')
        self.mock_create_user = self.create_user_patcher.start()
        
        self.authenticate_user_patcher = patch('main.authenticate_user')
        self.mock_authenticate_user = self.authenticate_user_patcher.start()
        
        # Mock encryption functions
        self.store_encrypted_password_patcher = patch('main.store_encrypted_password')
        self.mock_store_encrypted_password = self.store_encrypted_password_patcher.start()
        
        self.retrieve_encrypted_password_patcher = patch('main.retrieve_encrypted_password')
        self.mock_retrieve_encrypted_password = self.retrieve_encrypted_password_patcher.start()

    def tearDown(self):
        """Clean up after each test method."""
        self.init_db_patcher.stop()
        self.create_user_patcher.stop()
        self.authenticate_user_patcher.stop()
        self.store_encrypted_password_patcher.stop()
        self.retrieve_encrypted_password_patcher.stop()

    def simulate_input(self, input_values):
        """Helper method to simulate user input."""
        return patch('builtins.input', side_effect=input_values)

    def capture_output(self):
        """Helper method to capture stdout."""
        return patch('sys.stdout', new=StringIO())

    def test_failed_db_initialization(self):
        """Test program exit when database initialization fails."""
        self.mock_init_db.return_value = (None, None)
        
        with self.capture_output() as mock_output:
            main()
            
        self.assertIn("Failed to initialize database", mock_output.getvalue())

    def test_create_new_account(self):
        """Test creating a new user account."""
        input_values = ['2', 'testuser', 'testpass', '3']
        
        with self.simulate_input(input_values), self.capture_output():
            main()
            
        self.mock_create_user.assert_called_once_with(
            self.mock_cursor,
            self.mock_conn,
            'testuser',
            'testpass'
        )

    def test_successful_login_and_store_password(self):
        """Test successful login and storing a new password."""
        self.mock_authenticate_user.return_value = True
        input_values = [
            '1',              # Choose login
            'testuser',       # Username
            'testpass',       # Password
            '1',              # Choose store password
            'example.com',    # Site name
            'sitepass123',    # Site password
            '3',              # Logout
            '3'               # Exit program
        ]
        
        with self.simulate_input(input_values), self.capture_output():
            main()
            
        self.mock_authenticate_user.assert_called_once_with(
            self.mock_cursor,
            'testuser',
            'testpass'
        )
        self.mock_store_encrypted_password.assert_called_once_with(
            self.mock_cursor,
            self.mock_conn,
            'testuser',
            'example.com',
            'sitepass123',
            'testpass'
        )

    def test_retrieve_stored_password(self):
        """Test retrieving a stored password."""
        self.mock_authenticate_user.return_value = True
        self.mock_cursor.fetchall.return_value = [('example.com',)]
        self.mock_retrieve_encrypted_password.return_value = 'retrieved_password'
        
        input_values = [
            '1',              # Choose login
            'testuser',       # Username
            'testpass',       # Password
            '2',              # Choose retrieve password
            '1',              # Select first site
            '3',              # Logout
            '3'               # Exit program
        ]
        
        with self.simulate_input(input_values), self.capture_output() as mock_output:
            main()
            
        self.mock_retrieve_encrypted_password.assert_called_once_with(
            self.mock_cursor,
            'testuser',
            'example.com',
            'testpass'
        )
        self.assertIn("retrieved_password", mock_output.getvalue())

    def test_failed_login(self):
        """Test failed login attempt."""
        self.mock_authenticate_user.return_value = False
        input_values = [
            '1',          # Choose login
            'testuser',   # Username
            'wrongpass',  # Wrong password
            '3'          # Exit program
        ]
        
        with self.simulate_input(input_values), self.capture_output() as mock_output:
            main()
            
        self.assertIn("Login failed", mock_output.getvalue())

    def test_no_stored_passwords(self):
        """Test retrieving passwords when none are stored."""
        self.mock_authenticate_user.return_value = True
        self.mock_cursor.fetchall.return_value = []
        
        input_values = [
            '1',          # Choose login
            'testuser',   # Username
            'testpass',   # Password
            '2',          # Choose retrieve password
            '3',          # Logout
            '3'          # Exit program
        ]
        
        with self.simulate_input(input_values), self.capture_output() as mock_output:
            main()
            
        self.assertIn("No stored passwords found", mock_output.getvalue())

if __name__ == '__main__':
    unittest.main()
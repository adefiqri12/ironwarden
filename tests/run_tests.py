import unittest
import sys
import pathlib

# Add the project root directory to Python path
sys.path.append(str(pathlib.Path(__file__).parent))

# Import all test modules
from test_encryption import TestEncryption
from test_database import TestDatabase
from test_user import TestUser

def run_tests():
    # Create a test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestEncryption))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestDatabase))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestUser))
    
    # Run the test suite
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Return 0 if tests passed, 1 if any failed
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests())
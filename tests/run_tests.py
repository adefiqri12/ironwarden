import unittest
import sys
import os

# Ensure the root directory is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Debug: Print the sys.path to verify
print(sys.path)

# Now import the test cases
from tests.test_encryption import TestEncryption
from tests.test_database import TestDatabase
from tests.test_master_account import TestUser

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
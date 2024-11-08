from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
import time

# Simulated storage for master credentials (username and hashed master password)
user_database = {}

# Function to create a new user (username and hashed master password)
def create_user(username, master_password):
    # Generate a salt for hashing the master password
    salt = os.urandom(16)
    # Hash the master password with PBKDF2
    hashed_master_password = derive_key(master_password, salt)
    # Store the username, salt, and hashed password in the simulated database
    user_database[username] = {'salt': salt, 'hashed_password': hashed_master_password}
    print("User created successfully!")

# Function to authenticate the user
def authenticate_user(username, master_password):
    if username in user_database:
        # Retrieve stored salt and hashed password
        stored_data = user_database[username]
        stored_hashed_password = stored_data['hashed_password']
        salt = stored_data['salt']
        
        # Derive the key from the entered password and stored salt
        derived_key = derive_key(master_password, salt)
        
        # Verify if the derived key matches the stored hashed password
        if derived_key == stored_hashed_password:
            print("Authentication successful!")
            return True
        else:
            print("Incorrect password.")
    else:
        print("Username not found.")
    return False

# Function to derive a key from the master password using PBKDF2
def derive_key(password, salt, iterations=100000):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

# Function to encrypt a password
def encrypt_password(password, master_password):
    salt = os.urandom(16)
    key = derive_key(master_password, salt)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Padding the password to fit AES block size
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(password.encode()) + padder.finalize()
    encrypted_password = encryptor.update(padded_data) + encryptor.finalize()
    
    return {
        'salt': salt,
        'iv': iv,
        'encrypted_password': encrypted_password
    }

# Function to decrypt a password
def decrypt_password(encrypted_data, master_password):
    salt = encrypted_data['salt']
    iv = encrypted_data['iv']
    encrypted_password = encrypted_data['encrypted_password']
    
    key = derive_key(master_password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    padded_data = decryptor.update(encrypted_password) + decryptor.finalize()
    
    # Removing padding
    unpadder = padding.PKCS7(128).unpadder()
    password = unpadder.update(padded_data) + unpadder.finalize()
    return password.decode()

print("WELCOME")
# Create a new user
username = "my_username"
master_password = "my_master_password"
create_user(username, master_password)

# Attempt to authenticate
login_username = input("Enter your username: ")
login_password = input("Enter your master password: ")

start_time = time.time()
if authenticate_user(login_username, login_password):
    # Only proceed if the user is authenticated
    password_to_store = "my_secure_password"
    
    # Encrypt the password
    encrypted_data = encrypt_password(password_to_store, login_password)
    print("Encrypted password data:", encrypted_data)
    
    # Decrypt the password
    decrypted_password = decrypt_password(encrypted_data, login_password)
    print("Decrypted password:", decrypted_password)

    # Check decryption time
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
else:
    print("Access denied. Unable to access stored passwords.")

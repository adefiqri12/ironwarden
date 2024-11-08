import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Derive a key from the master password using PBKDF2
def derive_key(password, salt, iterations=100000):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

# Encrypt a password and store it in the database
def store_encrypted_password(cursor, conn, username, site_name, password, master_password):
    salt = os.urandom(16)
    key = derive_key(master_password, salt)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(password.encode()) + padder.finalize()
    encrypted_password = encryptor.update(padded_data) + encryptor.finalize()
    cursor.execute("INSERT INTO stored_passwords (username, site_name, salt, iv, encrypted_password) VALUES (?, ?, ?, ?, ?)",
                (username, site_name, salt, iv, encrypted_password))
    conn.commit()
    print(f"Password for '{site_name}' stored successfully!")

# Decrypt a password retrieved from the database
def retrieve_encrypted_password(cursor, username, site_name, master_password):
    cursor.execute("SELECT salt, iv, encrypted_password FROM stored_passwords WHERE username = ? AND site_name = ?", 
                (username, site_name))
    result = cursor.fetchone()
    if result:
        salt, iv, encrypted_password = result
        key = derive_key(master_password, salt)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(encrypted_password) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        password = unpadder.update(padded_data) + unpadder.finalize()
        return password.decode()
    else:
        print("No password found for this site.")
        return None
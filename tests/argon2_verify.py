from argon2 import PasswordHasher

ph = PasswordHasher()

# Input password
password = ""
# Stored hash (you provided this)
stored_hash = ""

# Verify the password against the hash
try:
    ph.verify(stored_hash, password)
    print("Password is correct")
except:
    print("Password is incorrect")

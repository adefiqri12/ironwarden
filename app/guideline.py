import re

def print_ascii_welcome():
    return print("""
██╗██████╗  ██████╗ ███╗   ██╗██╗    ██╗ █████╗ ██████╗ ██████╗ ███████╗███╗   ██╗
██║██╔══██╗██╔═══██╗████╗  ██║██║    ██║██╔══██╗██╔══██╗██╔══██╗██╔════╝████╗  ██║
██║██████╔╝██║   ██║██╔██╗ ██║██║ █╗ ██║███████║██████╔╝██║  ██║█████╗  ██╔██╗ ██║
██║██╔══██╗██║   ██║██║╚██╗██║██║███╗██║██╔══██║██╔══██╗██║  ██║██╔══╝  ██║╚██╗██║
██║██║  ██║╚██████╔╝██║ ╚████║╚███╔███╔╝██║  ██║██║  ██║██████╔╝███████╗██║ ╚████║
╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═══╝
    """)

def guideline():
    return print("""
Guideline for Creating a Username and Password
To keep your data secure, this program relies on a strong master password to encrypt
and decrypt stored passwords. Below is a simple guideline to help you create a 
strong and memorable username and password for your account.

Username Tips
1. Be Unique but Recognizable: Choose a username that’s easy for you to remember but
   not obvious to others, like "EchoTraveler2023" or "WinterTiger".
2. Avoid Predictable info: Don’t use your name or simple usernames like "admin" or 
   "user".

Password Tips
1. Avoid Predictable Info: Skip common details like birthdays, or simple passwords 
   like "Password123".
2. Use a Passphrase: Make a phrase memorable to you but hard to guess. Shorten it 
   with symbols and numbers, like "ILike2ReadBooks!" becomes "IL2RdBks!".
3. Mix Character Types: Use uppercase, lowercase, numbers, and symbols. Example: 
   "D4ncing@Sunrise2024!"
4. Aim for Length: 12–16 characters is ideal for security and memorability.

""")

def is_common_username(username, common_usernames):
    """Check if the username is a variation of any common usernames."""
    for common_username in common_usernames:
        # Create a regex pattern that matches the common username with any variations
        pattern = rf"^{common_username}[\d\W_]*$"  # \d matches digits, \W matches non-word characters
        if re.fullmatch(pattern, username.lower()):
            return True
    return False

def is_valid_username(username, common_usernames):
    """Check if the username meets guidelines and is not a common username."""
    if len(username) < 5:
        print("Username must be at least 5 characters.")
        return False
    if is_common_username(username, common_usernames):
        print(f"Username '{username}' is too similar to a common username.")
        return False
    if username.isnumeric():
        print("Username should not be purely numbers.")
        return False
    return True

def load_common_credentials(credential_type="username", filename=None):
    """Load common credentials from a file."""
    if filename is None:
        filename = f"./dictionary/common_{credential_type}.txt"
    try:
        with open(filename, "r", encoding='utf-8') as file:
            credentials = [line.strip().lower() for line in file]
        return credentials
    except FileNotFoundError:
        print(f"Warning: Common {credential_type} file not found at {filename}")
        return []
    except Exception as e:
        print(f"Error loading common {credential_type}s: {str(e)}")
        return []

def is_common_password(password, common_passwords):
    """Check if the password is a common password."""
    if password.lower() in common_passwords:
        print(f"Password '{password}' is too common or predictable.")
        return True
    return False

def is_strong_password(password, common_passwords):
    """Check if the password meets security guidelines."""
    if len(password) < 8 :
        print("Password should be at least 8 characters.")
        return False
    if not re.search(r'[A-Z]', password):
        print("Password should contain at least one uppercase letter.")
        return False
    if not re.search(r'[a-z]', password):
        print("Password should contain at least one lowercase letter.")
        return False
    if not re.search(r'[0-9]', password):
        print("Password should contain at least one digit.")
        return False
    if is_common_password(password, common_passwords):
        print(f"Password '{password}' is too similar to a common password.")
        return False
    return True
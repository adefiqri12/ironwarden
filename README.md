# IRONWARDEN

**IRONWARDEN** is a simple CLI-based password manager designed for secure storage and management of passwords in local desktop. Ironwarden securely stores and manages passwords using a combination of Argon2 hashing, AES encryption, and a SQLite database. 

When a user creates an account, their master password is hashed with Argon2 and stored in the database. Argon2 is designed to resist brute-force attacks by being memory-intensive, meaning it’s computationally expensive to crack.

For authentication, the entered password is verified against the stored hash. Individual site passwords are encrypted using AES with a key derived from the master password and a unique salt for each entry. The encrypted password, along with the salt and initialization vector (IV), is saved in the database. This ensures that both the master password and stored passwords are protected through strong encryption and hashing, even if the database is compromised. 

For a detailed explanation, refer to [how_it_works.txt](how_it_works.txt).

## Current Build
**Version**: v0.1

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Todo List](#todo-list)
- [Completed Features](#completed-features)
- [Planned Features](#planned-features)
- [Future Implementations](#future-implementations)


## Features

- **Login Setup**: Create a new account and log in to access the program.
- **SQLite Database**: Securely stores user data within a SQLite database.
- **Master Password**: Set a master password to protect all stored data.
- **Password Management**: Includes full CRUD (Create, Read, Update, Delete) operations for storing and managing passwords for various sites or IDs.


## Installation

### Running Directly in the Terminal

1. **Install Python 3.10+**  
   Ensure Python 3.10 or later is installed. [Download Python](https://www.python.org/downloads/).

2. **Install Dependencies**  
   Clone or download the repository, then navigate to the project directory and install dependencies with:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**  
   To launch the password manager, run the command :
   ```bash
   python app/main.py
   ```


### Creating an Executable (.exe) for Windows

To run as a standalone executable on Windows:

1. **Install Dependencies**  
   Install Python 3.10+ and then PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. **Add Scripts to PATH**  
   Add `C:\Users\<YourUsername>\AppData\Roaming\Python\Python310\Scripts` to your system’s `PATH` if not already done.

3. **Verify Installations**  
   Confirm Python and PyInstaller installation:
   ```bash
   python --version
   pip show pyinstaller
   ```

4. **Create Executable**  
   In the project directory, run:
   ```bash
   pyinstaller --onefile --name Ironwarden --icon=icon.ico app/main.py
   ```

5. **Locate Executable**  
   The generated executable will be in the `dist/` folder.


## Todo List

- [ ] Edit master password with a 12-word seed phrase.
- [ ] Create a one-click app to avoid terminal use.
- [ ] Enable cloud backup for database storage.
- [x] Add randomly generated, readable usernames with an expanded English dictionary.
- [ ] Implement automatic password generation with customizable options:
    - Only numbers (for PINs)
    - Lowercase only
    - Mixed case
    - Mixed case with numbers
    - Mixed case with numbers and special characters
- [ ] Add support for text-based data storage (e.g., notes).
- [ ] Implement a search feature for stored accounts.
- [ ] Lock access after 10 failed login attempts, with an option to recover using a 12-word seed phrase.
- [ ] Enable OTP-based 2FA (using `pyotp`) for enhanced security.


## Completed Features

- [x] Login setup with account creation.
- [x] Integrated SQLite database for data storage.
- [x] Added edit and delete options for stored passwords.
- [x] Passwords are hidden and directly pasted to reduce exposure.
- [x] Memory cleaning for secure password handling using `ctypes`.


## Planned Features

- **Cloud Backup**: Secure database backups to the cloud.
- **Readable Random Usernames**: Enhanced random username generator.
- **Automatic Password Creation**: Generate passwords based on predefined criteria.
- **Text-Based Data Storage**: Save notes and account-related information.
- **Search Functionality**: Quick search for stored accounts.


## Future Implementations

- **Device-Specific Salt**  
   Store a unique, device-specific salt locally. This device-bound salt, combined with the master password, ensures that encrypted passwords remain secure and accessible only from authorized devices.

- **Encrypted Backup and Recovery**  
   Add a secondary passphrase for backup restoration if primary credentials are lost after repeated login failures.

- **Enhanced Password Security with Pepper**  
   Incorporate a "pepper," an extra secret value stored outside the database, into the password hashing process. This additional security layer further protects against brute-force attacks in case of database breaches.

---
# IRONWARDEN
Password Manager Program v0.1
The Login system using Argon2

The stored data using 

Python 3.10

## Table of Contents
---------------
* [Features](#features)
* [Installation](#installation)
* [Planned Features](#planned-features)
* [First Todolist](#first-todolist)
* [Second Todolist](#second-todolist)

## Features
---------------

* **Login Setup**: Create a new account and login to the program
* **Sqlite Database**: Store user data securely in a SQLite database
* **Master Password**: Set a master password to secure your all data
* **Password Storage**: CRUD (Create, Read, Update, Delete) operations for storing passwords for different sites or IDs

## Installation
---------------

#### 1. **Running Directly in the Terminal**

1. **Install Python 3.10+**:
   - Ensure Python 3.10+ is installed. [Download Python](https://www.python.org/downloads/).

2. **Install Dependencies**:
   - Clone or download the repository.
   - Navigate to the project directory and install the required packages from `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```

3. **Run the Application**:
   - After installing the dependencies, run the password manager directly in the terminal:
     ```bash
     python app/main.py
     ```

---

#### 2. **Creating the Executable (.exe)**

If you prefer to create a standalone executable (`.exe`) for Windows without open the terminal, follow these steps:

1. **Install Dependencies**:
   - Ensure Python 3.10+ is installed. [Download Python](https://www.python.org/downloads/).
   - Install PyInstaller:
     ```bash
     pip install pyinstaller
     ```

2. **Add `Scripts` to `PATH`** (if not already done):
   - Add `C:\Users\<YourUsername>\AppData\Roaming\Python\Python310\Scripts` to your system’s `PATH` environment variable.

3. **Verify Installation**:
   - Check Python version:
     ```bash
     python --version
     ```
   - Ensure PyInstaller is installed:
     ```bash
     pip show pyinstaller
     ```

4. **Create Executable**:
   - Navigate to your project directory and run:
     ```bash
     pyinstaller --onefile --name Ironwarden --icon=icon.ico app/main.py
     ```

   If `pyinstaller` isn't recognized, try running with the full path:
   ```bash
   C:\Users\<YourUsername>\AppData\Roaming\Python\Python310\Scripts\pyinstaller --onefile --name Ironwarden --icon=icon.ico app/main.py
   ```

5. **Locate Executable**:
   - After the build completes, find the executable in the `dist/` folder.

## Planned Features
-------------------

* **Save Database to Cloud**: Save the database to cloud for backup
* **Random Generated Username**: Generate random readable usernames
* **Automated Password Creation**: Automatically create stored passwords using a dictionary
* **Text-Based Data Storage**: Store text-based data, such as notes and accounts
* **Searching Feature**: Add a searching feature for account search

## First Todolist
-----------------

- [x] Add login setup (create)
- [x] Add sqlite database
- [x] Edit and delete stored password
- [x] The Password will be not shown but automatically paste
- [x] Cleaning memory after master_password or stored password been call using os_urandom and ctypes
- [ ] Edit master password with 12 seed phrase
- [ ] Create one click app not run it from terminal

## Second Todolist
-----------------

- [ ] Save the database to cloud (for backup)
- [x] Random generated username (readable)
	+ Add more english noun into dictionary
- [ ] Automatically create the stored password using dictionary (it can be reloaded until user satisfaction)
- [ ] The automated created password, can be selected to include:
	+ only 6 number (for pin)
	+ only lowercase
	+ uppercase and lowercase
	+ uppercase, lowercase, and number 0-9
	+ uppercase, lowercase, number 0-9, and special character
- [ ] Add option to save text-based data, the program option look alike:
	+ save account and password
	+ save note/text
- [ ] Add searching feature for account search
- [ ] (?) Add login attempt to master password if failed 10 times, it will ask 12 word seedphrase
- [ ] Implement OTP for Two-Factor Authentication (2FA) using pyotp if master password forget

## Feature Implementation
-----------------

* **Utilize a Unique Device-Based Salt**: Generate and store a device-specific salt in addition to the one used in PBKDF2. This salt should be unique to each device the user logs in from and stored locally on that device. Combining the master password and device salt ensures that the encrypted passwords are bound to a specific device, limiting accessibility if the master password alone is compromised.

* **Encrypted Backup and Recovery of Encrypted Data**: If a user is locked out after 10 attempts and loses the recovery code, they should still be able to restore their data with a backup encrypted with a secondary password or passphrase.

* **Consider Using a Hash Function with Pepper for Master Password Verification**:A pepper is an additional value, stored separately from the password database (e.g., in the application code or in a secure environment variable). It can be added to the password before hashing, making it more difficult for an attacker to brute-force even if they gain access to the database. This method requires securely storing the pepper outside the database and only using it during authentication.
<img src="./ironwarden.png" alt="Ironwarden icon" width="100" height="100">

# IRONWARDEN
[![GitHub release](https://img.shields.io/badge/release-3.0.1-yellow.svg)](https://github.com/adefiqri12/ironwarden/releases/latest)
**Version**: v0.1.1 

**IRONWARDEN** is a simple CLI-based password manager designed for secure storage and management of passwords on a local desktop. IRONWARDEN securely stores and manages passwords using a combination of Argon2 hashing, AES encryption, and a SQLite database.

When a user creates an account, their master password is hashed with Argon2 and stored in the database. Argon2 is designed to resist brute-force attacks by being memory-intensive, making it computationally expensive to crack.

For authentication, the entered password is verified against the stored hash. Individual site passwords are encrypted using AES, with a key derived from the master password and a unique salt for each entry. The encrypted password, along with the salt and initialization vector (IV), is saved in the database. This ensures that both the master password and stored passwords are protected through strong encryption and hashing, even if the database is compromised.

For a detailed explanation, refer to [how_it_works.txt](how_it_works.txt).

### Features

- **Login Setup**: Create a new account and log in to access the program.
- **SQLite Database**: Securely stores user data within a SQLite database.
- **Master Password**: Set a master password to protect all stored data.
- **Password Management**: Includes full CRUD (Create, Read, Update, Delete) operations for storing and managing passwords for various sites or IDs.

## Table of Contents

- [Installation](#installation)
- [Complete Features](#completed-features)
- [Planned Features](#planned-features)
- [Disclaimer](#disclaimer)

## Installation

### Option 1: Running the `.exe` File (Recommended for Windows Users)

If you're on Windows, you can use the pre-built `.exe` file to quickly set up and run the application without needing Python installed.

1. **Download the `.exe` File**  
   Go to the [latest release](https://github.com/adefiqri12/ironwarden/releases/latest) and download the `ironwarden.exe` file.

2. **Run the Application**  
   Simply double-click the `ironwarden.exe` file to launch the application.  
   > **Note**: This will open the application in a command-line interface (CLI) window.

### Option 2: Running Directly from Source Code (Requires Python)

If you want to run the application from the source code or are not on Windows, follow the steps below.

1. **Download or Clone the Repository**  
   Download the `.zip` file from the [latest release](https://github.com/adefiqri12/ironwarden/releases/latest), or clone the repository directly with:
   ```bash
   git clone https://github.com/adefiqri12/ironwarden.git
   ```
   Extract or navigate to the project directory.

2. **Verify and Install Python 3.10+**  
   Ensure Python 3.10 or later is installed. Check your version with:
   ```bash
   python3 --version  # or `python --version` depending on your system
   ```
   If needed, download the latest version of Python [here](https://www.python.org/downloads/).

3. **Install Dependencies**  
   Navigate to the project directory and install dependencies with:
   ```bash
   cd ironwarden
   pip install -r requirements.txt
   ```

4. **Run the Application**  
   Make sure you’re in the `./ironwarden` directory before running the application. You can check your current directory by running:
   ```bash
   pwd  # prints the current directory path
   ```
   Once confirmed, launch the password manager by executing:
   ```bash
   python app/main.py
   ```

> **Note:** Running `python app/main.py` will only work if you’re in the `./ironwarden` directory, where `app/main.py` is located.

## Complete Features

- [x] Login setup with account creation.
- [x] Integrated SQLite database for data storage.
- [x] Added edit and delete options for stored passwords.
- [x] Passwords are hidden and directly pasted to reduce exposure.
- [x] Memory cleaning for secure password handling using `ctypes`.
- [x] Automatic password generation with custom length and customizable options:
    - Only numbers (for PINs)
    - Lowercase only
    - Mixed case
    - Mixed case with numbers
    - Mixed case with numbers and special characters

## Planned Features

- **Cloud Backup**: Secure database backups to the cloud.
- **Readable Random Usernames**: Enhanced random username generator.
- **Automatic Password Creation**: Generate passwords based on predefined criteria.
- **Text-Based Data Storage**: Save notes and account-related information.
- **Search Functionality**: Quick search for stored accounts.

### Future Implementations

- **Device-Specific Salt**  
   Store a unique, device-specific salt locally. This device-bound salt, combined with the master password, ensures that encrypted passwords remain secure and accessible only from authorized devices.

- **Encrypted Backup and Recovery**  
   Add a secondary passphrase for backup restoration if primary credentials are lost after repeated login failures.

- **Enhanced Password Security with Pepper**  
   Incorporate a "pepper," an extra secret value stored outside the database, into the password hashing process. This additional security layer further protects against brute-force attacks in case of database breaches.

- **AI-Biometric Security**  
   Integrate AI-powered biometric authentication methods (e.g. facial recognition, fingerprint recognition) to provide an additional layer of security for accessing the password manager.

### Todolist

- [ ] Edit master password with a 12-word seed phrase.
- [ ] Lock access after 10 failed login attempts, with an option to recover using a 12-word seed phrase.
- [ ] Enable cloud backup for database storage.
- [ ] Add randomly generated, readable usernames with an expanded English dictionary.
- [ ] Add support for text-based data storage (e.g., notes).
- [ ] Implement a search feature for stored accounts.
- [ ] Enable OTP-based 2FA (using `pyotp`) for enhanced security.

---

## Disclaimer

### USE AT YOUR OWN RISK

The author of this software is not responsible for any data created or lost while using this program. This program is provided "as-is" without warranty of any kind, express or implied. By using this program, you acknowledge that you understand and agree to this disclaimer.

You are responsible for ensuring the security and integrity of your data. The author is not liable for any damages or losses resulting from the use of this program.

### BACK UP YOUR DATA REGULARLY

It is your responsibility to regularly back up your data to prevent loss in case of software failure or other unforeseen circumstances.

By using this program, you acknowledge that you have read and understood this warning and disclaimer.

### TROUBLESHOOTING

IRONWARDEN is actively in development. If you find a bug, have a question or want to request a new feature, please [open an issue](https://github.com/adefiqri12/ironwarden/issues) and we will address it as soon as possible. 

You can also propose changes via a Pull Request: fork the repository, make your changes, and send us a Pull Request. We'll review it shortly. 

---
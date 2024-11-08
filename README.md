# IRONWARDEN
Password Manager Program v0.1
The Login system using Argon2

The stored data using 

Python 3.10

## Table of Contents
---------------

* [Features](#features)
* [Planned Features](#planned-features)
* [First Todolist](#first-todolist)
* [Second Todolist](#second-todolist)

## Features
---------------

* **Login Setup**: Create a new account and login to the program
* **Sqlite Database**: Store user data securely in a SQLite database
* **Master Password**: Set a master password to secure your all data
* **Password Storage**: CRUD (Create, Read, Update, Delete) operations for storing passwords for different sites or IDs

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
- [x] Add id and email to corresponding stored password
- [x] Edit stored password
- [x] The Password will be not shown but automatically paste
- [x] Cleaning memory after master_password or stored password been call using os_urandom and ctypes
- [ ] Edit master password with 12 seed phrase

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
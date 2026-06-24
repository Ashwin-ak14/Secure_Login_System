# Secure Login System

A Flask-based web application that provides secure user registration and login functionality using bcrypt password hashing and SQLite database storage.

## Features

* User Registration and Login
* Secure Password Hashing with Bcrypt
* SQL Injection Protection
* Session Management
* Logout Functionality
* Input Validation

## Technologies Used

* Python
* Flask
* Flask-Bcrypt
* SQLite

## Installation

```bash
pip install flask flask-bcrypt
python app.py
```

Open: `http://127.0.0.1:5000`

## Security Features

* Passwords are stored as hashed values.
* Parameterized SQL queries prevent SQL injection.
* Flask sessions manage authenticated users securely.
* Basic password validation is implemented.

## Future Enhancements

* Two-Factor Authentication (2FA)
* Password Reset Feature
* Email Verification
* Strong Password Policies



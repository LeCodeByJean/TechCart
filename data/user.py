"""
This module defines the User class and related functions for user management.

The User class represents a user in the TechCart application and
provides methods for user creation, password verification, and email retrieval.

Functions:
- create(username, email, clear_password, role='customer'): Creates a new User object.
- validate_email(email): Validates the format of an email address.
- validate_password_strength(clear_password): Validates the strength of a password.

Attributes:
- username (str): The username of the user.
- encrypted_email (str): The encrypted email of the user.
- password_hash (str): The hashed password of the user.
- salt (str): The salt used for password hashing.
- role (str): The role of the user.
- encrypted_user_key (str): The encrypted user key used for data encryption.
- cart (dict): The user's shopping cart.

Interdependencies:
- This module uses the utility/security module for data encryption and decryption.
- This module uses the utility/password_security module for password hashing and verification.

"""

import re  # Regular expression (RegEx) module for email validation
from utility.logger import setup_logger
from utility.security import (
    encrypt_data, decrypt_data, generate_key,
    get_or_create_master_key, encrypt_user_key, decrypt_user_key
)
from utility.password_security import generate_salt, hash_password, check_password

# Initialize the logger
logger = setup_logger('user_log')

class User:
    """
    Represents a user in the TechCart application.
    """

    def __init__(self, username, encrypted_email, password_hash, salt, role, encrypted_user_key):
        """
        Initializes a User object.

        Args:
            username (str): The username of the user.
            encrypted_email (str): The encrypted email of the user.
            password_hash (str): The hashed password of the user.
            salt (str): The salt used for password hashing.
            role (str): The role of the user (default: 'customer').
            encrypted_user_key (str): The encrypted user key used for data encryption.

        Attributes:
            username (str): The username of the user.
            encrypted_email (str): The encrypted email of the user.
            password_hash (str): The hashed password of the user.
            salt (str): The salt used for password hashing.
            role (str): The role of the user.
            encrypted_user_key (str): The encrypted user key used for data encryption.
            cart (dict): The user's shopping cart.

        """
        self.username = username
        self.encrypted_email = encrypted_email
        self.password_hash = password_hash
        self.salt = salt
        self.role = role
        self.encrypted_user_key = encrypted_user_key
        self.cart = {}  # Initialize an empty cart

    @classmethod
    def create(cls, username, email, clear_password, role='customer'):
        """
        Creates a new User object.

        Args:
            username (str): The username of the user.
            email (str): The email of the user.
            clear_password (str): The clear password of the user.
            role (str, optional): The role of the user (default: 'customer').

        Returns:
            User: The newly created User object.

        Raises:
            ValueError: If the email format is invalid or the password does not meet the strength requirements.

        """
        if not cls.validate_email(email):
            logger.error("Invalid email format for user: %s", username)
            raise ValueError("Invalid email format")
        if not cls.validate_password_strength(clear_password):
            logger.error("Password does not meet strength requirements for user: %s", username)
            raise ValueError("Password does not meet strength requirements")

        master_key = get_or_create_master_key()
        user_key = generate_key()
        encrypted_user_key = encrypt_user_key(user_key, master_key)
        encrypted_email = encrypt_data(email, user_key)
        salt = generate_salt()
        password_hash = hash_password(clear_password, salt)
        user = cls(username, encrypted_email, password_hash, salt, role, encrypted_user_key)
        logger.info("New user created: %s", username)
        return user

    @staticmethod
    def validate_email(email):
        """
        Validates the format of an email address.

        Args:
            email (str): The email address to validate.

        Returns:
            bool: True if the email format is valid, False otherwise.

        """
        return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

    @staticmethod
    def validate_password_strength(clear_password):
        """
        Validates the strength of a password. The password must:
        - Be at least 8 characters long
        - Contain at least one digit
        - Contain at least one lowercase letter
        - Contain at least one uppercase letter
        - Contain at least one special character (!@#$%^&*()-_+=)

        Args:
            clear_password (str): The password to validate.

        Returns:
            bool: True if the password meets the strength requirements, False otherwise.

        """
        special_characters = set("!@#$%^&*()-_+=")
        logger.debug("Validating password strength: %s", clear_password)
        is_valid = (
            len(clear_password) >= 8 and
            any(char.isdigit() for char in clear_password) and
            any(char.islower() for char in clear_password) and
            any(char.isupper() for char in clear_password) and
            any(char in special_characters for char in clear_password)
        )

        if not is_valid:
            logger.error(
                "Password validation failed. Password not strong enough: Length: %d, Has Digit: %s, "
                "Has Lowercase: %s, Has Uppercase: %s, Has Special Char: %s",
                len(clear_password),
                any(char.isdigit() for char in clear_password),
                any(char.islower() for char in clear_password),
                any(char.isupper() for char in clear_password),
                any(char in special_characters for char in clear_password)
            )

        return is_valid

    def verify_password(self, clear_password):
        """
        Verifies if a given password matches the user's password.

        Args:
            clear_password (str): The password to verify.

        Returns:
            bool: True if the password is correct, False otherwise.

        """
        is_correct = check_password(self.password_hash, self.salt, clear_password)
        logger.debug(
            "Password verification for user %s: %s", self.username,
            "successful" if is_correct else "failed"
        )
        return is_correct

    def get_email(self):
        """
        Decrypts and retrieves the user's email.

        Returns:
            str: The decrypted email of the user.

        """
        master_key = get_or_create_master_key()
        user_key = decrypt_user_key(self.encrypted_user_key, master_key)
        email = decrypt_data(self.encrypted_email, user_key)
        logger.debug("Email retrieved for user %s", self.username)
        return email

    def __str__(self):
        """
        Returns a string representation of the User object.

        Returns:
            str: The string representation of the User object.

        """
        return f'User(username="{self.username}", role="{self.role}")'

# End of data/user.py
"""
This module provides functionalities for secure password management. 
It includes methods for generating salts, hashing passwords using SHA-256 with a salt, and verifying 
hashed passwords against provided passwords.

Functions:
- generate_salt(): Generates a unique salt using UUID.
- hash_password(clear_password, salt): Hashes a password with the specified salt using SHA-256.
- check_password(stored_password_hash, salt, provided_password): Verifies a 
provided password against a stored hash and salt.

Safety focus:
    What: Secure password management using salted hashing.
    Why: To protect user passwords from being compromised in case of a data breach.
    How: The passwords are hashed using a secure hashing algorithm (SHA-256) with a
    unique salt added for each user. This makes it computationally expensive for attackers
    to crack the passwords even if they have the hashed values.

        * SHA-256 is a cryptographic hash function that produces a 256-bit (32-byte) hash value.
          It's an asymmetric algorithm meaning that the same input will always produce the
          same output, but the output cannot be reversed to obtain the original input.

        * The added salt ensures that even if two users have the same password, the
        hashed values will be different. This prevents attackers from using precomputed
        dictionary attacks or rainbow table attacks to crack the passwords.
"""

import hashlib # Secure 256-bit Hash Algorithm Library
import uuid # Universal Unique Identifier used for salting here
from utility.logger import setup_logger

# Initialize the logger
logger = setup_logger('password_sec_log')

def generate_salt(): 
    """
    Generates a random salt using UUID.
    
    Returns:
        str: A unique salt as a hexadecimal string.
    """
    return uuid.uuid4().hex # Return the UUID as a hexadecimal string

def hash_password(clear_password, salt):
    """
    Hashes the password using SHA-256 with a provided salt.

    Args:
        clear_password (str): The password to be hashed.
        salt (str): The salt used in the hashing process.

    Returns:
        str: The hashed password as a hexadecimal string.
    """
    return hashlib.sha256(salt.encode() + clear_password.encode()).hexdigest()

def check_password(stored_password_hash, salt, provided_password):
    """
    Verifies if the provided password matches the stored hash.
    
    Args:
        stored_password_hash (str): The stored password hash to be compared.
        salt (str): The salt used in the hashing process.
        provided_password (str): The password to be verified.
        
    Returns:     
        bool: True if the provided password matches the stored hash, False otherwise.
    
    """
    return stored_password_hash == hashlib.sha256(salt.encode() + provided_password.encode()).hexdigest()

# End of utility/password_security.py

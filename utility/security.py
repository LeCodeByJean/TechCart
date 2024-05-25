"""
This module provides functions for encryption and decryption of data using
the Fernet symmetric encryption algorithm.

Functions:
- generate_key(): Generates a new encryption key and returns it.
- save_key(key, key_path): Saves the encryption key to a file.
- load_key(key_path): Loads the encryption key from a file.
- get_or_create_master_key(): Loads the master key, generating it if it doesn't exist.
- encrypt_data(data, key): Encrypts data using the provided key.
- decrypt_data(encrypted_data, key): Decrypts data using the provided key.
- encrypt_user_key(user_key, master_key): Encrypts a user's key using the master key.
- decrypt_user_key(encrypted_user_key, master_key): Decrypts a user's key using the master key.

Attributes:
- MASTER_KEY_PATH (str): The path to the master key file.

Safety focus:
    What: Encryption and decryption of user's data using the Fernet symmetric encryption algorithm.
    Why: To protect sensitive data from unauthorized access.
    How: The encryption key is used to encrypt the user's data, and the master key is used to encrypt the encryption keys.
    It provides two layers of encryption for added security.
"""
import os
from cryptography.fernet import Fernet
from utility.logger import setup_logger

# Initialize the logger
logger = setup_logger('security_log')

MASTER_KEY_PATH = 'master.key'

def generate_key():
    """
    Generates a new encryption key and returns it.

    Returns:
        bytes: The encryption key.
    """
    return Fernet.generate_key()

def save_key(key, key_path):
    """
    Saves the encryption key to a file.
    
    Parameters:
        key (bytes): The encryption key.
        key_path (str): The path to the key file.
    """
    with open(key_path, 'wb') as key_file:
        key_file.write(key)

def load_key(key_path):
    """
    Loads the encryption key from a file.

    Parameters:
        key_path (str): The path to the key file.

    Returns:
        bytes: The encryption key.
    """
    if not os.path.exists(key_path):
        raise FileNotFoundError(f"No such file or directory: '{key_path}'")

    with open(key_path, 'rb') as key_file:
        key = key_file.read()

    return key

def get_or_create_master_key():
    """
    Loads the master key, generating it if it doesn't exist.
    The master key is used to encrypt and decrypt user keys. It's a second layer of encryption.
    
    Returns:
        bytes: The master encryption key.
    """
    if not os.path.exists(MASTER_KEY_PATH):
        master_key = generate_key()
        save_key(master_key, MASTER_KEY_PATH)
    else:
        master_key = load_key(MASTER_KEY_PATH)

    return master_key

def encrypt_data(data, key):
    """
    Encrypts data using the provided key.

    Parameters:
        data (str): The data to encrypt.
        key (bytes): The encryption key.

    Returns:
        bytes: The encrypted data.
    """
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data, key):
    """
    Decrypts data using the provided key.

    Parameters:
        encrypted_data (bytes): The data to decrypt.
        key (bytes): The encryption key.

    Returns:
        str: The decrypted data.
    """
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data).decode()
    return decrypted_data

def encrypt_user_key(user_key, master_key):
    """
    Encrypts a user's key using the master key.

    Parameters:
        user_key (bytes): The user's encryption key.
        master_key (bytes): The master encryption key.

    Returns:
        bytes: The encrypted user key.
    """
    fernet = Fernet(master_key)
    encrypted_user_key = fernet.encrypt(user_key)
    return encrypted_user_key

def decrypt_user_key(encrypted_user_key, master_key):
    """
    Decrypts a user's key using the master key.

    Parameters:
        encrypted_user_key (bytes): The encrypted user key.
        master_key (bytes): The master encryption key.

    Returns:
        bytes: The decrypted user key.
    """
    fernet = Fernet(master_key)
    user_key = fernet.decrypt(encrypted_user_key)
    return user_key

# End of utility/security.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from utility.password_security import generate_salt, hash_password, check_password

def test_generate_salt():
    salt = generate_salt()
    assert isinstance(salt, str)
    assert len(salt) == 32  # UUID4 hex string length is 32

def test_hash_password():
    salt = generate_salt()
    password = "Aa12345!"
    hashed_password = hash_password(password, salt)
    
    assert isinstance(hashed_password, str)
    assert len(hashed_password) == 64  # SHA-256 hex string length is 64

def test_check_password():
    salt = generate_salt()
    password = "Aa12345!"
    hashed_password = hash_password(password, salt)
    
    # Correct password
    assert check_password(hashed_password, salt, password) is True
    
    # Incorrect password
    assert check_password(hashed_password, salt, "wrong_password") is False

def test_hashing_same_password_different_salts():
    password = "Aa12345!"
    salt1 = generate_salt()
    salt2 = generate_salt()
    
    hashed_password1 = hash_password(password, salt1)
    hashed_password2 = hash_password(password, salt2)
    
    assert hashed_password1 != hashed_password2

def test_hashing_different_passwords_same_salt():
    salt = generate_salt()
    password1 = "Aa12345!1"
    password2 = "Aa12345!2"
    
    hashed_password1 = hash_password(password1, salt)
    hashed_password2 = hash_password(password2, salt)
    
    assert hashed_password1 != hashed_password2

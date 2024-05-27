import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from unittest.mock import patch
from data.user import User

# Sample data for tests
username = "UserTest"
email = "user@email.com"
clear_password = "Aa12345!"
role = "customer"
salt = "randomsalt123"
password_hash = "hashedpassword"
encrypted_email = b"encryptedemail"
encrypted_user_key = b"encrypteduserkey"

@pytest.fixture
def mock_security():
    with patch("data.user.get_or_create_master_key", return_value="masterkey"), \
         patch("data.user.generate_key", return_value="userkey"), \
         patch("data.user.encrypt_user_key", return_value=encrypted_user_key), \
         patch("data.user.encrypt_data", return_value=encrypted_email), \
         patch("data.user.generate_salt", return_value=salt), \
         patch("data.user.hash_password", return_value=password_hash), \
         patch("data.user.decrypt_user_key", return_value="userkey"), \
         patch("data.user.decrypt_data", return_value=email):
        yield

def test_user_creation(mock_security):
    user = User.create(username, email, clear_password, role)
    assert user.username == username
    assert user.encrypted_email == encrypted_email
    assert user.password_hash == password_hash
    assert user.salt == salt
    assert user.role == role
    assert user.encrypted_user_key == encrypted_user_key

def test_validate_email():
    assert User.validate_email("user@email.com")
    assert not User.validate_email("invalid.email.com")

def test_validate_password_strength():
    assert User.validate_password_strength("Aa12345!")
    assert not User.validate_password_strength("weak")

def test_verify_password(mock_security):
    user = User.create(username, email, clear_password, role)
    with patch("data.user.check_password", return_value=True) as mock_check_password:
        assert user.verify_password(clear_password)
        mock_check_password.assert_called_once_with(password_hash, salt, clear_password)

def test_get_email(mock_security):
    user = User.create(username, email, clear_password, role)
    assert user.get_email() == email

def test_user_str(mock_security):
    user = User.create(username, email, clear_password, role)
    assert str(user) == f'User(username="{username}", role="{role}")'

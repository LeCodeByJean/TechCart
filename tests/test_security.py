import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import os
import pytest
from cryptography.fernet import Fernet
from utility.security import (
    generate_key, save_key, load_key, get_or_create_master_key,
    encrypt_data, decrypt_data, encrypt_user_key, decrypt_user_key,
    MASTER_KEY_PATH
)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Remove master key file if it exists
    if os.path.exists(MASTER_KEY_PATH):
        os.remove(MASTER_KEY_PATH)
    yield
    #Teardown: Remove master key file if it was created during tests
    if os.path.exists(MASTER_KEY_PATH):
        os.remove(MASTER_KEY_PATH)

def test_generate_key():
    key = generate_key()
    assert isinstance(key, bytes)
    assert len(key) == 44 # Fernet key length

def test_save_and_load_key():
    key = generate_key()
    key_path = 'test.key'
    save_key(key, key_path)
    loaded_key = load_key(key_path)
    assert key == loaded_key
    os.remove(key_path)

def test_load_key_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_key('non_existent.key')

def test_get_or_create_master_key():
    key = get_or_create_master_key()
    assert isinstance(key, bytes)
    assert len(key) == 44
    # Check if the master key file was created
    assert os.path.exists(MASTER_KEY_PATH)
    loaded_key = load_key(MASTER_KEY_PATH)
    assert key == loaded_key

def test_encrypt_and_decrypt_data():
    key = generate_key()
    data = "sensitive data"
    encrypted_data = encrypt_data(data, key)
    assert isinstance(encrypted_data, bytes)
    decrypted_data = decrypt_data(encrypted_data, key)
    assert decrypted_data == data

def test_encrypt_and_decrypt_user_key():
    master_key = generate_key()
    user_key = generate_key()
    encrypted_user_key = encrypt_user_key(user_key, master_key)
    assert isinstance(encrypted_user_key, bytes)
    decrypted_user_key = decrypt_user_key(encrypted_user_key, master_key)
    assert decrypted_user_key == user_key

if __name__ == "__main__":
    pytest.main()
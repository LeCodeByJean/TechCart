"""
This module provides functions to manage a user database.

The user database is stored in a dictionary called 'users', where
the keys are usernames and the values are User objects.

Functions:
- add_user(user): Adds a user to the database.
- get_user(username): Retrieves a user from the database.
- update_user(username, **kwargs): Updates the attributes of a user in the database.
- delete_user(username): Deletes a user from the database.
"""

from data.user import User
from utility.logger import setup_logger

# Initialize the logger
logger = setup_logger('user_db_log')
users = {}

def add_user(user):
    """
    Adds a user to the database.

    Args:
        user (User): The user object to be added.

    Returns:
        bool: True if the user was added successfully, False otherwise.

    Raises:
        ValueError: If the user already exists in the database.
    """
    username = user.username
    if username in users:
        logger.error("Attempt to add a user that already exists: %s", username)
        raise ValueError("User already exists")
    users[username] = user
    logger.info("User added successfully: %s", username)
    return True

def get_user(username):
    """
    Retrieves a user from the database.

    Args:
        username (str): The username of the user to retrieve.

    Returns:
        User: The user object if found, None otherwise.
    """
    user = users.get(username)
    if user:
        logger.info("User retrieved: %s", username)
    else:
        logger.warning("User not found: %s", username)
    return user

def update_user(username, **kwargs):
    """
    Updates the attributes of a user in the database.

    Args:
        username (str): The username of the user to update.
        **kwargs: Keyword arguments representing the attributes to update.

    Returns:
        bool: True if the user was updated successfully, False otherwise.
    """
    if username not in users:
        logger.warning("Attempt to update non-existing user: %s", username)
        return False
    user = users[username]
    for key, value in kwargs.items():
        if hasattr(user, key):
            setattr(user, key, value)
            logger.info("User updated %s: %s -> %s", username, key, value)
    return True

def delete_user(username):
    """
    Deletes a user from the database.

    Args:
        username (str): The username of the user to delete.

    Returns:
        bool: True if the user was deleted successfully, False otherwise.
    """
    if username in users:
        del users[username]
        logger.info("User deleted: %s", username)
        return True
    logger.warning("Attempt to delete non-existing user: %s", username)
    return False

# End of data/user_db.py

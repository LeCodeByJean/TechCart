"""
This module provides authentication services with integrated two-factor authentication (2FA).
It includes the `AuthenticationService` class, which handles user registration and authentication.
It logs failed login attempts and implements conditional two-factor authentication
after 3 failed attempts.
The `AuthenticationService` class provides the following functionalities:

Functions:
- `register_user` method: Registers a new user with the provided credentials.
- `authenticate_user` method: Authenticates a user by verifying their credentials and handling 2FA.

Attributes:
- `storage` attribute: The storage object used to store user data.
- `failed_attempts` attribute: A dictionary to track failed login attempts.
- `locked_accounts` attribute: A dictionary to track locked user accounts.
- `_2fa_verified` attribute: A boolean flag to indicate successful 2FA verification.

The module also includes the following helper functions:

- `register_user` function: Registers a new user.
- `login_user` function: Logs in a user by verifying their credentials.

Interdependencies:
- `getpass` from the Python standard library for password input masking (hidden input)
- `data.user` module for the `User` class and the `validate_email` and
`validate_password_strength` functions
- `data.user_db` module for the `add_user` and `get_user` functions
- `utility.two_factor_auth` module for the `generate_security_code` and
`send_security_code` functions
- `utility.password_security` module for the `generate_salt`, `hash_password`,
and `check_password` functions
- `utility.security` module for the `get_or_create_master_key`, `generate_key`,
`encrypt_user_key`, and `encrypt_data` functions
- `utility.logger` module for the `setup_logger` function

Safety focus:
    What: Strong password requirement, secure password storage, and two-factor authentication.
    Why: To ensure secure user authentication and protect user accounts from unauthorized access.
    How: By enforcing strong password requirements, email adress validation, securely stores user passwords, and implements 2FA.
"""
import getpass
from data.user import User
from data.user_db import add_user, get_user
from utility.two_factor_auth import generate_security_code, send_security_code
from utility.password_security import generate_salt, hash_password, check_password
from utility.security import get_or_create_master_key, generate_key, encrypt_user_key, encrypt_data
from utility.logger import setup_logger

# Initialize the logger
logger = setup_logger('authentication_process_log')

class AuthenticationService:
    """
    Provides authentication services with integrated two-factor authentication
    after three failed login attempts, and account locking after five failed login attempts.
    This class ensures that user login attempts are verified against stored credentials
    and handles conditional two-factor authentication if multiple failed attempts are detected.
    """

    def __init__(self, storage):
        self.storage = storage
        self.failed_attempts = {}
        self.locked_accounts = {}
        self._2fa_verified = False

    def register_user(self, username, clear_password, email, role='customer', encrypted_user_key=None):
        """
        Registers a new user with the provided credentials.
        
        Parameters:

        - `username` (str): The username of the new user.
        - `clear_password` (str): The password of the new user.
        - `email` (str): The email of the new user.
        - `role` (str, optional): The role of the new user (default: 'customer').
        - `encrypted_user_key` (str, optional): The encrypted user key for the new user.

        Returns:
        - User: The User object for the newly registered user.

        Raises:
        - ValueError: If the user already exists, the email format is invalid,
        or the password does not meet the strength requirements.
        """
        logger.debug("Attempting to register user with username: %s, email: %s, role: %s", username, email, role)

        if username in self.storage:
            logger.error("User already exists: %s", username)
            raise ValueError("User already exists")
        if not User.validate_email(email):
            logger.error("Invalid email format: %s", email)
            raise ValueError("Invalid email format")

        if not User.validate_password_strength(clear_password):
            logger.error("Password validation failed for user: %s", username)
            raise ValueError("Password does not meet strength requirements")

        try:
            salt = generate_salt()
            hashed_password = hash_password(clear_password, salt)
            master_key = get_or_create_master_key()
            user_key = generate_key()
            encrypted_user_key = encrypt_user_key(user_key, master_key)
            encrypted_email = encrypt_data(email, user_key)

            new_user = User(
                username=username,
                password_hash=hashed_password,
                salt=salt,
                encrypted_email=encrypted_email,
                role=role,
                encrypted_user_key=encrypted_user_key
            )
            add_user(new_user)
            logger.info("Registered new user with username: %s", username)
            return new_user
        except Exception as e:
            logger.error("User registration failed for %s: %s", username, str(e))
            raise

    def authenticate_user(self, username, clear_password, security_code=None):
        """
        Authenticates a user by verifying their credentials and handling 2FA if necessary.

        Parameters:
        - `username` (str): The username of the user.
        - `clear_password` (str): The password provided by the user.
        - `security_code` (str, optional): The 2FA code provided by the user.

        Returns:
        - bool: True if authentication is successful, False otherwise.
        """
        logger.debug("Attempting to authenticate user: %s", username)
        user = get_user(username)

        if not user:
            logger.warning("User not found: %s", username)
            return False
       
        if username in self.failed_attempts and self.failed_attempts[username]['locked']:
            if security_code and security_code == self.failed_attempts[username]['code']:
                logger.info("2FA code matches, verifying password...")
                entered_password = getpass.getpass("Enter password (hidden input): ")
                if check_password(user.password_hash, user.salt, entered_password):
                    logger.info("Password verified, authenticating user...")
                    del self.failed_attempts[username]
                    self._2fa_verified = True
                    # Reset failed attempts count and "unlock" the account
                    self.failed_attempts[username] = {'count': 0, 'locked': False, 'code': None}
                    logger.info("2FA code verified successfully for user: %s", username)
                    return True
                else:
                    logger.info("User authentication failed for %s : incorrect password.", username)
                    return False
            else:
                logger.warning("2FA check failed for user: %s", username)
                return False

        if check_password(user.password_hash, user.salt, clear_password): 
            if username in self.failed_attempts:
                del self.failed_attempts[username]
            logger.info("User authenticated successfully: %s", username)
            return True
        else:
            self._log_failed_attempt(user)
            logger.info("User authentication failed for %s : incorrect password.", username)
            return False

    def _log_failed_attempt(self, user):
        username = user.username

        if username not in self.failed_attempts:
            self.failed_attempts[username] = {'count': 1, 'locked': False, 'code': None} # Initialize failed attempt count
        else:
            self.failed_attempts[username]['count'] += 1 # Increment failed attempt count
            logger.info("Failed atempt count: %i", self.failed_attempts[username]['count'])
            if self.failed_attempts[username]['count'] >= 3 and not self.failed_attempts[username]['locked'] and not self._2fa_verified:
                self.failed_attempts[username]['locked'] = True
                security_code = generate_security_code()
                self.failed_attempts[username]['code'] = security_code
                send_security_code(user.get_email(), security_code)
                logger.info("2FA code sent to user: %s", username)


def register_user(username, clear_password, email, role='customer', encrypted_user_key=None):
    """
    Registers a new user.

    Parameters:
        username (str): The username for the new user.
        clear_password (str): The password for the new user.
        email (str): The email for the new user.
        role (str, optional): The role of the new user, defaults to 'customer'.
        encrypted_user_key (str, optional): The encrypted user key for the new user.

    Returns:
        bool: True if registration is successful, False otherwise.
    """
    logger.debug("Registering user with username: %s, email: %s, role: %s", username, email, role)
    logger.debug("Password entered (clear_password): %s", clear_password)
    if not User.validate_password_strength(clear_password):
        logger.error("Password validation failed. Password not strong enough: Length: %d, Has Digit: %s, Has Lowercase: %s, Has Uppercase: %s, Has Special Char: %s",
                     len(clear_password),
                     any(char.isdigit() for char in clear_password),
                     any(char.islower() for char in clear_password),
                     any(char.isupper() for char in clear_password),
                     any(char in "!@#$%^&*()-_+=" for char in clear_password))
        return False

    logger.debug("Password validation successful for user: %s", username)

    try:
        salt = generate_salt()
        logger.debug("Generated salt (salt): %s", salt)

        hashed_password = hash_password(clear_password, salt)
        logger.debug("Hashed password (hashed_password): %s", hashed_password)

        master_key = get_or_create_master_key()
        logger.debug("Retrieved/Generated master key")

        user_key = generate_key()
        logger.debug("Generated user key")

        encrypted_user_key = encrypt_user_key(user_key, master_key)
        logger.debug("Encrypted user key")

        encrypted_email = encrypt_data(email, user_key)
        logger.debug("Encrypted email")

        new_user = User(
            username=username,
            password_hash=hashed_password,
            salt=salt,
            encrypted_email=encrypted_email,
            role=role,
            encrypted_user_key=encrypted_user_key
        )
        add_user(new_user)
        logger.info("User registration successful for %s", username)
        return True
    except Exception as e:
        logger.error("User registration failed for %s: %s", username, str(e))
        return False

def login_user(username, clear_password):
    """
    Logs in a user by verifying their credentials.

    Parameters:
        username (str): The username of the user attempting to log in.
        clear_password (str): The password provided by the user during the login attempt.

    Returns:
        User: The User object if login is successful, None otherwise.
    """
    logger.debug("Attempting to log in user: %s", username)
    user_data = get_user(username)
    if user_data:
        user = User(
            username=user_data.username,
            encrypted_email=user_data.encrypted_email,
            password_hash=user_data.password_hash,
            salt=user_data.salt,
            role=user_data.role,
            encrypted_user_key=user_data.encrypted_user_key
        )
        if check_password(user.password_hash, user.salt, clear_password):
            logger.info("User login successful for %s", username)
            return user
        else:
            logger.warning("User login failed for %s: Incorrect password", username)
            return None
    else:
        logger.warning("User login failed for %s: User not found", username)
        return None

# end of services/authentication_process.py

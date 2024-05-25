"""
This module provides functionality for two-factor authentication (2FA) as part of the security
measures. It includes generating a unique security code and the 
capability to send this code to a user's email address to verify their identity following multiple 
failed login attempts.

Functions:
    generate_security_code(): Generates a six-digit numeric security code.
    send_security_code(email, code): Sends the generated code to the specified email address.
    
Note:
    This module does not send actual emails.
    It is for demonstration purposes only.
    It simulates the 2FA code sent to the user's email by print it in the log file.

Safety focus:
    What: The 2FA code that generated randomly and sent to the user's email.
    Why: To provide an additional layer of security for user authentication.
    How: The code sent to the user's email for verification becomes a mandatory
    additional step for the user to access the system.
"""

import random
from utility.logger import setup_logger

# Initialize the logger
logger = setup_logger('2fa_log')

def generate_security_code():
    """
    Generates a six-digit numeric security code for two-factor authentication.
    
    Returns:
        str: The generated security code.
    """
    return f"{random.randint(100000, 999999)}" # 6-digit random number

def send_security_code(email, code):
    """
    Simulates sending the generated security code to the user's email.
    
    Parameters:
        email (str): The email address to send the code to.
        code (str): The security code to send.
    """
    logger.info("Simulation of email with the 2FA code. Check logs/techcart.log to see the code.")
    logger.debug("EMAIL SIMULATION : The 2FA code for %s is: %s", email, code)

# End of utility/two_factor_auth.py

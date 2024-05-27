"""
Module: config.py

Holds configuration settings for the TechCart software.
"""

import os

class Config:
    """
    Configuration settings for TechCart.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    DEBUG = os.environ.get('DEBUG', 'True') == 'True'
    LOG_FILE = os.environ.get('LOG_FILE', 'logs/techcart.log')
    PAYMENT_KEY_PATH = os.environ.get('PAYMENT_KEY_PATH', 'path_to_payment_key')
    RATE_LIMIT = os.environ.get('RATE_LIMIT', '100 per day;10 per hour') #  Rate limit for API requests



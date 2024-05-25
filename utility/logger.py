"""
This module sets up centralized logging. It configures
logging to output to both the console and a file, using a rotating file handler to
manage log sizes. The logger outputs INFO level messages to the console and DEBUG
level messages to a file.

Functions:
- setup_logger(): Sets up centralized logging for the TechCart application, providing
dual output to console and file with a rotating file handler to manage log sizes.

Usage:
    Directly call setup_logger(log_file='path/to/logfile') to initialize
    logging in any part of the application.
"""

import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name, log_file='./logs/techcart.log'):
    """
    Sets up centralized logging for the TechCart application, providing dual
    output to console and file with a rotating file handler to manage log sizes.
    
    This function configures a logger to output INFO level messages to the console
    and DEBUG level messages to a file, suitable for both development and 
    production diagnostics.

    Parameters:
        name (str): Name of the logger.
        log_file (str): Path to the default log file.

    Returns:
        A configured logger instance with console and file handlers.
    """
    # Create logger with a specific name and set its level to DEBUG
    app_logger = logging.getLogger(name)
    app_logger.setLevel(logging.DEBUG)

    # Define log message format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    # Console handler setup for INFO level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Ensure the directory for log files exists
    log_directory = os.path.dirname(log_file)
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # File handler setup with rotation, for DEBUG level
    file_handler = RotatingFileHandler(
        log_file, maxBytes=1024*1024*1, backupCount=5 # 1MB file size, 5 backup files
        )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    app_logger.addHandler(console_handler)
    app_logger.addHandler(file_handler)

    return app_logger

# End of utility/logger.py

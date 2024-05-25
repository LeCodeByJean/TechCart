'''
This module provides functions for processing payments by asking the user 
their credit card information and validating it.

Functions:
- process_payment(): Process the payment by asking the user for their credit card information and validating it.

Note: This module does not perform actual payment processing. It is for demonstration purposes only.
'''

import hashlib
import os
from datetime import datetime
from utility.logger import setup_logger

# Initialize the logger
logger = setup_logger('payment_process_log')

def process_payment():
    """
    Process the payment by asking the user for their credit card information and validating it.

    Returns:
        str: The status of the payment. It can be either "approved" or "declined".
    """
    logger.info("--------we are in payment_process.process_payment--------")
    # Ask the user for their credit card info and validate the data
    cardholder_name = input("Enter cardholder name: ")
    if not cardholder_name:
        logger.error("Missing cardholder name")
        return "declined"
    card_number = input("Enter card number (16 digits): ")
    if not (len(card_number) == 16 and card_number.isdigit() ):
        logger.error("Invalid card number")
        return "declined"
    expiry_month = input("Enter the two digits for expiry month(MM): ")
    if not (len(expiry_month) == 2 and expiry_month.isdigit()):
        logger.error("Invalid expiry month format")
        return "declined"
    expiry_year = input("Enter the two digits for expiry year(YY): ")
    if not (len(expiry_year) == 2 and expiry_year.isdigit()):
        logger.error("Invalid expiry year format")
        return "declined"
    cvv = input("Enter CVV: ")
    if not (len(cvv) == 3 and cvv.isdigit()):
        logger.error("Invalid CVV format")
        return "declined"

    # Check if the card is expired
    expiry_yyyy = int(expiry_year) + 2000
    expiry_mm = int(expiry_month)
    current_month, current_year = datetime.now().strftime("%m/%Y").split("/")
    if int(expiry_yyyy) < int(current_year):
        logger.error(
            "Card is expired (year). Year of the card: %s, current year: %s",
            expiry_yyyy, current_year
            )
        return "declined"
    elif (int(expiry_yyyy) == int(current_year) and int(expiry_mm) < int(current_month)):
        logger.error(
            "Card is expired (month). Month of the card: %s, current month: %s",
            expiry_month, current_month
            )
        return "declined"
    else:
        # Hash the payment info
        payment_info = f"{cardholder_name}{card_number}{expiry_month}{expiry_year}{cvv}"
        salt = os.urandom(16)
        # hashed_payment_info not used since there is no real payment processing for this assignment
        hashed_payment_info = hashlib.pbkdf2_hmac('sha256', payment_info.encode(), salt, 100000)
        logger.info("Payment processed successfully")
        return "approved"

    # End service/payment_process.py

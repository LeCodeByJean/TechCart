"""
This module contains the Order class, which represents an order placed by a user.

Classes:
    Order: Represents an order placed by a user.

Functions:
    None

Attributes:
    logger (Logger): The logger object used for logging order-related events.
"""

import uuid
from datetime import datetime
from utility.logger import setup_logger

# Initialize the logger
logger = setup_logger('order_log')

class Order:
    """
    Represents an order placed by a user.

    Attributes:
        order_id (str): The unique identifier for the order.
        user_id (str): The ID of the user placing the order.
        items (list): A list of items (product_id, quantity) in the order.
        total_amount (float): The total amount for the order.
        status (str): The status of the order.
        created_at (datetime): The date and time when the order was created.
        updated_at (datetime): The date and time when the order was last updated.

    Methods:
        __init__(user_id, items, total_amount, status='pending'): Initializes a new order instance.
        update_status(new_status): Updates the status of the order.
        to_dict(): Serializes the order to a dictionary.
    """

    def __init__(self, user_id, items, total_amount, status='pending'):
        """
        Initializes a new order instance.

        Parameters:
            user_id (str): The ID of the user placing the order.
            items (list): A list of items (product_id, quantity) in the order.
            total_amount (float): The total amount for the order.
            status (str): The status of the order (default is 'pending').

        Returns:
            None
        """
        self.order_id = str(uuid.uuid4())  # Generate a unique order ID
        self.user_id = user_id
        self.items = items
        self.total_amount = total_amount
        self.status = status
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        logger.info("Order instance created with Order ID: %s", self.order_id)

    # This function is currently not in use, only designed for future integration.
    def update_status(self, new_status):
        """
        Updates the status of the order.

        Parameters:
            new_status (str): The new status of the order.

        Returns:
            None
        """
        self.status = new_status
        self.updated_at = datetime.now()
        logger.info("Order ID %s status updated to %s", self.order_id, self.status)

    def to_dict(self):
        """
        Serializes the order to a dictionary.

        Returns:
            dict: A dictionary containing the order details.
        """
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "items": self.items,
            "total_amount": self.total_amount,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

# End of data/order.py

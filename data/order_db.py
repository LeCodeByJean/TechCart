"""
This module contains the functions to interact with the order storage dictionary.

Functions:
    add_order(order): Adds a new order to the storage dictionary.
    get_order(order_id): Retrieves an order from the storage dictionary by Order ID.
    update_order(order_id, **kwargs): Updates the specified attributes of an 
    order in the storage dictionary.
    delete_order(order_id): Deletes an order from the storage dictionary by Order ID.

Classes:
    None

Exceptions:
    None

Attributes:
    orders (dict): The storage dictionary containing the orders.
    logger (Logger): The logger object used for logging order-related events.
"""

from datetime import datetime
from data.order import Order
from utility.logger import setup_logger

# Initialize the logger
logger = setup_logger('order_db_log')

# Initialize the order storage as a dictionary
orders = {}

def add_order(order):
    """
    Adds a new order to the storage dictionary.
    
    Parameters:
        order (Order): The order object to be added.

    Returns:
        dict: The serialized order dictionary.
    """
    orders[order.order_id] = order.to_dict()
    logger.info("Order added with Order ID: %s", order.order_id)
    return order.to_dict()

def get_order(order_id):
    """
    Retrieves an order from the storage dictionary by Order ID.

    Parameters:
        order_id (str): The ID of the order to retrieve.

    Returns:
        dict: The serialized order dictionary if found, None otherwise.
    """
    order = orders.get(order_id)
    if order:
        logger.info("Order retrieved with Order ID: %s", order_id)
    else:
        logger.warning("Order not found with Order ID: %s", order_id)
    return order

def update_order(order_id, **kwargs):
    """
    Updates the specified attributes of an order in the storage dictionary.

    Parameters:
        order_id (str): The ID of the order to update.
        **kwargs: The key-value pairs of the attributes to update.

    Returns:
        dict: The updated serialized order dictionary if the order exists, None otherwise.
    """
    if order_id in orders:
        order = orders[order_id]
        for key, value in kwargs.items():
            if key in order:
                order[key] = value
                logger.info("Order ID %s updated field %s to %s", order_id, key, value)
        order['updated_at'] = datetime.now().isoformat()
        return order
    logger.warning("Attempted to update non-existing order with Order ID: %s", order_id)
    return None

def delete_order(order_id):
    """
    Deletes an order from the storage dictionary by Order ID.

    Parameters:
        order_id (str): The ID of the order to delete.

    Returns:
        bool: True if the order was deleted, False otherwise.
    """
    if order_id in orders:
        del orders[order_id]
        logger.info("Order deleted with Order ID: %s", order_id)
        return True
    logger.warning("Attempted to delete non-existing order with Order ID: %s", order_id)
    return False

# End of data/order_db.py

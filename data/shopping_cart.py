"""
This module contains functions for managing shopping carts.

The module provides the following functions:
- rate_limit_check(user_id, action_type, limit, period): Checks if the user has exceeded the
rate limit for a specific action.
- add_item_to_cart(user_id, product_id, quantity): Adds an item to the user's shopping cart.
- remove_item_from_cart(user_id, product_id): Removes an item from the user's shopping cart.
- update_item_quantity_in_cart(user_id, product_id, quantity): Updates the quantity of an item 
in the user's shopping cart.
- view_cart(user_id): Views the contents of the user's shopping cart.
- clear_cart(user_id): Clears all items from the user's shopping cart.

The module also contains the following global variables:
- guest_carts: A dictionary to store guest user carts temporarily.
- action_tracker: A dictionary to track user actions for rate limiting.

Interdependencies:
- This module interacts with the user_db and product_db modules to retrieve
user and product information.
"""

import time
from data.user_db import get_user, update_user
from data.product_db import get_product
from utility.logger import setup_logger

# Initialize the logger
logger = setup_logger('shopping_cart_log')

# Dictionary to store guest user carts temporarily
guest_carts = {}
# Dictionary to track user actions for rate limiting
action_tracker = {
    'registration': {},
    'cart_actions': {}
}

def rate_limit_check(user_id, action_type, limit, period):
    """
    Checks if the user has exceeded the rate limit for a specific action.

    Args:
        user_id (str): The ID of the user.
        action_type (str): The type of action being performed.
        limit (int): The maximum number of actions allowed within the specified period.
        period (int): The time period (in seconds) within which the actions are counted.

    Returns:
        bool: True if the user is within the rate limit, False otherwise.
    """
    now = time.time()
    if user_id not in action_tracker[action_type]:
        action_tracker[action_type][user_id] = []

    # Filter out actions outside the rate limit period
    action_tracker[action_type][user_id] = [
        timestamp for timestamp in action_tracker[action_type][user_id]
        if now - timestamp < period
    ]

    if len(action_tracker[action_type][user_id]) >= limit:
        return False

    action_tracker[action_type][user_id].append(now)
    return True

def add_item_to_cart(user_id, product_id, quantity):
    """
    Adds an item to the user's shopping cart.

    Args:
        user_id (str): The ID of the user.
        product_id (str): The ID of the product to add.
        quantity (int): The quantity of the product to add.

    Returns:
        bool: True if the item was successfully added, False otherwise.
    """
    if not rate_limit_check(user_id, 'cart_actions', limit=10, period=60):
        logger.warning("Rate limit exceeded for user %s", user_id)
        return False

    if user_id:
        user = get_user(user_id)
        if not user:
            logger.error("User not found: %s", user_id)
            return False
        cart = user.cart
    else:
        if 'guest' not in guest_carts:
            guest_carts['guest'] = {}
        cart = guest_carts['guest']

    product = get_product(product_id)
    if not product:
        logger.error("Product not found: %s", product_id)
        return False

    if product['stock'] < quantity:
        logger.error("Insufficient stock for product %s", product_id)
        return False

    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity

    if cart[product_id] <= 0:
        cart.pop(product_id)

    if user_id:
        update_user(user_id, cart=cart)
    else:
        guest_carts['guest'] = cart

    logger.info("Added %s of product %s to cart", quantity, product_id)
    return True

def remove_item_from_cart(user_id, product_id):
    """
    Removes an item from the user's shopping cart.

    Args:
        user_id (str): The ID of the user.
        product_id (str): The ID of the product to remove.

    Returns:
        bool: True if the item was successfully removed, False otherwise.
    """
    if not rate_limit_check(user_id, 'cart_actions', limit=10, period=60):
        logger.warning("Rate limit exceeded for user %s", user_id)
        return False

    if user_id:
        user = get_user(user_id)
        if not user or product_id not in user.cart:
            logger.error(
                "Attempt to remove non-existent product %s from user %s's cart",
                product_id,
                user_id
            )
            return False
        del user.cart[product_id]
        update_user(user_id, cart=user.cart)
    else:
        if 'guest' not in guest_carts or product_id not in guest_carts['guest']:
            logger.error("Attempt to remove non-existent product %s from guest cart", product_id)
            return False
        del guest_carts['guest'][product_id]

    logger.info("Removed product %s from cart", product_id)
    return True

def update_item_quantity_in_cart(user_id, product_id, quantity):
    """
    Updates the quantity of an item in the user's shopping cart.

    Args:
        user_id (str): The ID of the user.
        product_id (str): The ID of the product to update.
        quantity (int): The new quantity of the product.

    Returns:
        bool: True if the quantity was successfully updated, False otherwise.
    """
    if not rate_limit_check(user_id, 'cart_actions', limit=10, period=60):
        logger.warning("Rate limit exceeded for user %s", user_id)
        return False

    if quantity <= 0:
        return remove_item_from_cart(user_id, product_id)

    if user_id:
        user = get_user(user_id)
        if not user:
            logger.error("User not found for ID %s", user_id)
            return False
        user.cart[product_id] = quantity
        update_user(user_id, cart=user.cart)
    else:
        if 'guest' not in guest_carts:
            guest_carts['guest'] = {}
        guest_carts['guest'][product_id] = quantity

    logger.info("Updated quantity of product %s to %s in cart", product_id, quantity)
    return True

def view_cart(user_id):
    """
    Views the contents of the user's shopping cart.

    Args:
        user_id (str): The ID of the user.

    Returns:
        dict: A dictionary representing the user's shopping cart.
    """
    if user_id:
        user = get_user(user_id)
        if not user:
            logger.error("User not found for ID %s", user_id)
            return {}
        return user.cart
    else:
        return guest_carts.get('guest', {})

def clear_cart(user_id):
    """
    Clears all items from the user's shopping cart.

    Args:
        user_id (str): The ID of the user.

    Returns:
        bool: True if the cart was successfully cleared, False otherwise.
    """
    if not rate_limit_check(user_id, 'cart_actions', limit=10, period=60):
        logger.warning("Rate limit exceeded for user %s", user_id)
        return False

    if user_id:
        if not get_user(user_id):
            logger.error("User not found for ID %s", user_id)
            return False
        update_user(user_id, cart={})
    else:
        guest_carts['guest'] = {}

    logger.info("Cleared all items from cart")
    return True

# End of data/shopping_cart.py

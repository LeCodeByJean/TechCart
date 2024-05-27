"""
This module provides functions for creating and updating orders.

Functions:
- create_order(user_id): Creates a new order with the items from the user's shopping
cart, processes payment, and updates stock quantities.
- update_order_status(order_id, new_status): Updates the status of an existing order.
- calculate_total_amount(cart): Calculates the total amount for the items in the cart.
- update_stock(items): Updates the stock quantities for the items in the order.

Attributes:
- logger: A logger object that is used to record log messages.

Interdependencies:
- utility.logger: This module is used to set up logging for the order process.
- data.order: This module is used to create instances of the Order class.
- data.order_db: This module is used to add and update orders in the database.
- data.shopping_cart: This module is used to view and clear the user's shopping cart.
- data.product_db: This module is used to get and update product information in the database.
- services.payment_process: This module is used to process payments for orders.
"""
from utility.logger import setup_logger
from data.order import Order
from data.order_db import add_order, update_order
from data.shopping_cart import view_cart, clear_cart
from data.product_db import get_product, update_product
#from services.payment_process import process_payment

# Set up logging
logger = setup_logger('order_process_log')

def create_order(user_id, payment_status):
    """
    Create an order for the given user ID.

    Args:
        user_id (int): The ID of the user.
        payment_status (str): The status of the payment, either "approved" or "declined".

    Returns:
        dict: A dictionary representing the order details.
    """
    logger.info("--------we are in order_process.create_order--------")

    # Retrieve the user's cart
    cart = view_cart(user_id)

    # Check if the cart is empty
    if not cart:
        logger.error("Cannot create order: Shopping cart is empty for user ID %s", user_id)
        return None

    # Prepare the items for the order
    items = [
        {
            "product_id": product_id,
            "quantity": quantity
        } for product_id, quantity in cart.items()
    ]

    # Calculate the total amount of the order
    total_amount = calculate_total_amount(cart)

    # Handle payment status
    if payment_status == "declined":
        order = Order(user_id, items, total_amount, status="declined")
        add_order(order)
        logger.warning("Order declined for user ID: %s", user_id)
        print(f"Payment status: {order.status}")
        return order.to_dict()
    elif payment_status == "approved":
        order = Order(user_id, items, total_amount, status="completed")
        logger.debug("-----we are in order_process.create_order - payment_status == approved-----")
        add_order(order)
        clear_cart(user_id)
        update_stock(items)
        logger.info("Order created and cart cleared for user ID: %s", user_id)
        print(f"Payment status: {order.status}")
        return order.to_dict()

def update_order_status(order_id, new_status):
    """
    Update the status of an order.

    Args:
        order_id (int): The ID of the order to update.
        new_status (str): The new status to set for the order.

    Returns:
        dict: The updated order details if the update was successful, otherwise None.

    """
    order = update_order(order_id, status=new_status)
    if order:
        logger.info("Order ID %s status updated to %s", order_id, new_status)
    return order

def calculate_total_amount(cart):
    """
    Calculate the total amount of the products in the cart.

    Args:
        cart (dict): A dictionary representing the cart, where the keys are product IDs and the values are quantities.

    Returns:
        float: The total amount of the products in the cart.

    """
    total = 0.0 # Initialize total amount a 0 float
    for product_id, quantity in cart.items():
        product = get_product(product_id)
        if product:
            total += product['price'] * quantity
    return total

def update_stock(items):
    """
    Update the stock levels of products based on the items in an order.

    Args:
        items (list): A list of dictionaries representing the items in the order, where each dictionary contains
        the product ID and the quantity ordered.

    Returns:
        None
    """
    for item in items:
        product_id = item['product_id']
        quantity = item['quantity']
        product = get_product(product_id)
        if product:
            new_stock = product['stock'] - quantity
            update_product(product_id, stock=new_stock)
            logger.info(
                "Updated stock for product ID %s: new stock level is %d",
                product_id, new_stock
            )

# End of order_process.py

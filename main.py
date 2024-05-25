"""
This module contains the main functionality for a tech e-commerce platform.
It provides a command-line interface for users to login, register, browse products,
add items to cart, and place orders.
The module consists of the following classes, functions, and methods:

Functions:
- cli(): Displays the main menu for customer users.
- login(): Login an existing user.
- register(): Register a new user.
- user_menu(): Displays the user menu after login or registration.
- guest_menu(): Displays the guest menu.
- view_items_guest_menu(): Displays the available items for guest users.
- view_items_menu(): Displays the available items to logged-in users and provides
options to add items to the cart.
- add_to_cart(): Add an item to the user's cart.
- view_cart_menu(): Displays the user's cart and provides options to remove items,
clear the cart, or place an order.
- remove_from_cart(): Remove an item from the user's cart.
- clear_user_cart(): Clear the user's cart.
- checkout(): Checkout the user's cart and create an order.

Attributes:
- user_state: A dictionary to store the logged-in user's ID.
- storage: A dictionary to store user data.
- auth_service: An instance of the AuthenticationService class for user authentication.

Interdependencies:
- The module depends on the following modules:
    - click: A package for creating command-line interfaces.
    - utility.logger: A module for setting up logging.
    - services.authentication_process: A module for user authentication.
    - services.order_process: A module for creating orders.
    - services.payment_process: A module for processing payments.
    - data.product_db: A module for accessing product data.
    - data.shopping_cart: A module for managing the shopping cart.
"""
import click
from utility.logger import setup_logger
from services.authentication_process import AuthenticationService
from services.order_process import create_order, calculate_total_amount
from services.payment_process import process_payment
from data.product_db import get_all_products
from data.shopping_cart import add_item_to_cart, view_cart, clear_cart, remove_item_from_cart

# Set up logging
logger = setup_logger('main_log')

# Global state to store logged in user's ID
user_state = {
    "logged_in_user": None
}

# Initialize storage and authentication service
storage = {}
auth_service = AuthenticationService(storage)

# Set up logging
logger = setup_logger('main_log')

# Global state to store logged in user's ID
user_state = {
    "logged_in_user": None
}

# Initialize storage and authentication service
storage = {}
auth_service = AuthenticationService(storage)

@click.group(invoke_without_command=True)
def cli():
    """
    Displays the main menu for customer users.

    The main menu provides options for users to login, register, browse products,
    and interact with their cart.
    """
    ascii_art = r"""
     _    _      _                            _          _____         _     _____            _   _ 
    | |  | |    | |                          | |        |_   _|       | |   /  __ \          | | | |
    | |  | | ___| | ___ ___  _ __ ___   ___  | |_ ___     | | ___  ___| |__ | /  \/ __ _ _ __| |_| |
    | |/\| |/ _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \    | |/ _ \/ __| '_ \| |    / _` | '__| __| |
    \  /\  /  __/ | (_| (_) | | | | | |  __/ | || (_) |   | |  __/ (__| | | | \__/\ (_| | |  | |_|_|
     \/  \/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/    \_/\___|\___|_| |_|\____/\__,_|_|   \__(_)
       by jean-G De Souza                                                                                         
"""
    click.echo(ascii_art)
    click.echo("This is a tech e-commerce platform where you can view and purchase tech products.")

    while True:
        click.echo("\nPlease choose an option:")
        click.echo("1. Login")
        click.echo("2. Create an account")
        click.echo("3. Browse as a guest")
        click.echo("4. Exit")
        choice = click.prompt("Enter your choice", type=int)

        if choice == 1:
            if login():
                user_menu()
        elif choice == 2:
            if register():
                user_menu()
        elif choice == 3:
            guest_menu()
        elif choice == 4:
            break
        else:
            click.echo("Invalid choice. Please try again.")

def login():
    """
    Login an existing user.

    Returns:
        bool: True if login is successful, False otherwise.
    """
    username = click.prompt("Enter username")
    password = click.prompt("Enter password", hide_input=True)
    
    if not auth_service.authenticate_user(username, password):
        if auth_service.failed_attempts.get(username, {}).get('locked', False):
            security_code = click.prompt("Enter the 2FA security code sent to your email")
            if auth_service.authenticate_user(username, password, security_code):
                auth_service.failed_attempts[username]['locked'] = False  # Reset locked status
                user_state["logged_in_user"] = username
                click.echo("Login successful.")
                return True
            else:
                click.echo("2FA failed. Login unsuccessful.")
                return False
        else:
            click.echo("Login failed.")
            return False
    else:
        user_state["logged_in_user"] = username
        click.echo("Login successful.")
        return True

def register():
    """
    Register a new user.

    Returns:
        bool: True if registration is successful, False otherwise.
    """
    username = click.prompt("Enter username")
    email = click.prompt("Enter email")
    # Display password requirements
    click.echo("""
    Please choose a password that meets the following criteria:
    - At least 8 characters long
    - Contains at least 1 digit
    - Contains at least one lowercase letter
    - Contains at least one uppercase letter
    - Contains at least one special character from the set !@#$%^&*()-_+=""
    """)
    password = click.prompt("Enter password (hidden input) ", hide_input=True)
    try:
        auth_service.register_user(username, password, email)
        click.echo("User registered successfully.")
        user_state["logged_in_user"] = username
        return True
    except ValueError as e:
        click.echo(f"Registration failed: {e}")
        return False

def user_menu():
    """
    Displays the user menu after login or registration.
    The user menu provides options to view available items, view the cart, and logout.
    """
    while True:
        click.echo("\nUser Menu:")
        click.echo("1. View our available items")
        click.echo("2. View my cart")
        click.echo("3. Logout")
        choice = click.prompt("Enter your choice", type=int)

        if choice == 1:
            view_items_menu()
        elif choice == 2:
            view_cart_menu()
        elif choice == 3:
            user_state["logged_in_user"] = None # Logout
            break
        else:
            click.echo("Invalid choice. Please try again.")

def guest_menu():
    """
    Displays the guest menu.
    The guest menu provides options to view available items, create an account, or go back to the previous menu.
    """
    while True:
        click.echo("\nGuest Menu:")
        click.echo("1. View our available items")
        click.echo("2. Create an account to save your cart")
        click.echo("3. Go back to previous menu")
        choice = click.prompt("Enter your choice", type=int)

        if choice == 1:
            view_items_guest_menu()
        elif choice == 2:
            if register():
                user_menu()
        elif choice == 3:
            break
        else:
            click.echo("Invalid choice. Please try again.")

def view_items_guest_menu():
    """
    Displays the available items and provides options to add items to the cart.
    This menu is for guest users who have not logged in.
    """
    click.echo("\nAvailable Items:")
    for sku, product in get_all_products().items():
        click.echo(
            f"SKU: {sku} | "
            f"Name: {product['name']} | "
            f"Price: {product['price']} | "
            f"Stock: {product['stock']}"
        )
    while True:
        click.echo("\nOptions:")
        click.echo("1. Create an account to save your cart")
        click.echo("2. Go back to previous menu")
        choice = click.prompt("Enter your choice", type=int)

        if choice == 1:
            if register():
                user_menu()
        elif choice == 2:
            break
        else:
            click.echo("Invalid choice. Please try again.")


def view_items_menu(guest=False):
    """
    Displays the available items and provides options to add items to the cart.

    Args:
        guest (bool): A flag to indicate if the user is a guest.
    """
    click.echo("\nAvailable Items:")
    for sku, product in get_all_products().items():
        click.echo(
            f"SKU: {sku} | "
            f"Name: {product['name']} | "
            f"Price: {product['price']} | "
            f"Stock: {product['stock']}"
        )

    while True:
        click.echo("\nOptions:")
        click.echo("1. Add an item to the cart")
        click.echo("2. Go back to previous menu")
        choice = click.prompt("Enter your choice", type=int)

        if choice == 1:
            add_to_cart(guest=guest)
        elif choice == 2:
            break
        else:
            click.echo("Invalid choice. Please try again.")

def add_to_cart(guest=False):
    """
    Add an item to the user's cart.

    Args:
        guest (bool): A flag to indicate if the user is a guest.
    """
    user_id = "guest" if guest else user_state["logged_in_user"]
    product_id = click.prompt("Enter product SKU to add to cart")
    quantity = click.prompt("Enter quantity", type=int)
    if add_item_to_cart(user_id, product_id, quantity):
        click.echo("Item added to cart.")
    else:
        click.echo("Failed to add item to cart.")

def view_cart_menu(guest=False):
    """
    Displays the user's cart and provides options to remove items, clear
    the cart, or place an order.

    Args:
        guest (bool): A flag to indicate if the user is a guest.
    """
    user_id = "guest" if guest else user_state["logged_in_user"]

    while True:
        cart = view_cart(user_id)
        if cart:
            click.echo("\nYour Cart:")
            for product_id, quantity in cart.items():
                click.echo(f"Product ID: {product_id}, Quantity: {quantity}")
            total_amount = calculate_total_amount(cart)
            click.echo(f"Total Cart Amount: {total_amount}")
        else:
            click.echo("Your cart is empty.")

        click.echo("\nCart Options:")
        click.echo("1. Remove an item from the cart")
        click.echo("2. Clear the cart")
        click.echo("3. Place order")
        click.echo("4. Go back to previous menu")
        choice = click.prompt("Enter your choice", type=int)

        if choice == 1:
            remove_from_cart(guest=guest)
        elif choice == 2:
            clear_user_cart(guest=guest)
        elif choice == 3:
            checkout(guest=guest)
        elif choice == 4:
            break
        else:
            click.echo("Invalid choice. Please try again.")

def remove_from_cart(guest=False):
    """
    Remove an item from the user's cart.

    Args:
        guest (bool): A flag to indicate if the user is a guest.
    """
    user_id = "guest" if guest else user_state["logged_in_user"]
    product_id = click.prompt("Enter product SKU to remove from cart")
    if remove_item_from_cart(user_id, product_id):
        click.echo("Item removed from cart.")
    else:
        click.echo("Failed to remove item from cart.")

def clear_user_cart(guest=False):
    """
    Clear the user's cart.
    
    Args:
        guest (bool): A flag to indicate if the user is a guest.
    """
    user_id = "guest" if guest else user_state["logged_in_user"]
    if clear_cart(user_id):
        click.echo("Cart cleared.")
    else:
        click.echo("Failed to clear cart.")

def checkout(guest=False):
    """
    Checkout the user's cart and create an order.

    Args:
        guest (bool): A flag to indicate if the user is a guest.
    """
    logger.info("--------we are in main.checkout--------") # Log the checkout process
    user_id = "guest" if guest else user_state["logged_in_user"]
    order = create_order(user_id)

    payment_status = process_payment()
    logger.debug("bool payment approved: %s", payment_status == "approved")
    if order and (payment_status == "approved"):
        click.echo(f"Order created successfully. Order ID: {order['order_id']}")
        click.echo("Thank you for shopping with us! You order will arrive soon. Maybe.")
        return
    else:
        click.echo("Payment declined. Order not placed.")
        click.echo("Checkout failed.")
        return

if __name__ == '__main__':
    cli.main()

# End of main.py

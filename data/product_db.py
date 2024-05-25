"""
This module provides functions to interact with the product storage dictionary.

Functions:
    add_product(name, description, price, stock): Adds a new product to the storage dictionary.
    get_product(sku): Retrieves a product from the storage dictionary by SKU.
    update_product(sku, **kwargs): Updates the specified attributes of a product 
    in the storage dictionary.
    delete_product(sku): Deletes a product from the storage dictionary by SKU.
    get_all_products(): Retrieves all products from the storage dictionary.

Attributes:
    logger (Logger): The logger object used for logging product-related events.
    products (dict): The dictionary containing product information.
"""
from data.product import Product
from utility.logger import setup_logger

# Initialize the logger
logger = setup_logger('product_db_log')

# Initialize the product storage as a dictionary
products = {
    "4db99f54-fadd-4bb7-a49d-db419beded14": {"name": "Logitech MX Vertical Mouse", "description": "A vertical mouse designed to reduce wrist strain.", "price": 99.99, "stock": 100},
    "5ea9c417-5b7d-4b96-b5b8-8a2d1bdc3b5e": {"name": "Keychron K3 Keyboard", "description": "A compact mechanical keyboard using low profile switches.", "price": 74.99, "stock": 100},
    "9c4e3178-1b23-1fr6-f35b-1b3ferdc3we3": {"name": "Neumann BCM 104 Microphone", "description": "Broadcast microphone for studio-quality sound.", "price": 699.90, "stock": 100},
}

def add_product(name, description, price, stock):
    """
    Add a new product to the product database.

    Args:
        name (str): The name of the product.
        description (str): The description of the product.
        price (float): The price of the product.
        stock (int): The stock quantity of the product.

    Returns:
        dict: A dictionary representing the added product.

    """
    product = Product.create(name, description, price, stock)
    products[product.sku] = product.to_dict()
    logger.debug("Product added with SKU: %s, Name: %s", product.sku, name)
    return product.to_dict()

def get_product(sku):
    """
    Retrieve a product from the product database by SKU.

    Args:
        sku (str): The SKU of the product to retrieve.

    Returns:
        dict: A dictionary representing the retrieved product, or None if not found.
    """
    product = products.get(sku)
    if product:
        logger.info("Product retrieved with SKU: %s", sku)
    else:
        logger.warning("Product not found with SKU: %s", sku)
    return product

def update_product(sku, **kwargs):
    """
    Update the specified attributes of a product in the product database.

    Args:
        sku (str): The SKU of the product to update.
        **kwargs: The keyword arguments representing the fields to update.

    Returns:
        dict: A dictionary representing the updated product, or None if the product does not exist.
    """
    if sku in products:
        updated = []
        if 'name' in kwargs:
            products[sku]['name'] = kwargs['name']
            updated.append('name')
        if 'description' in kwargs:
            products[sku]['description'] = kwargs['description']
            updated.append('description')
        if 'price' in kwargs:
            products[sku]['price'] = kwargs['price']
            updated.append('price')
        if 'stock' in kwargs:
            products[sku]['stock'] = kwargs['stock']
            updated.append('stock')
        logger.info("Product updated with SKU: %s, Updated fields: %s", sku, ', '.join(updated))
        return products[sku]
    logger.warning("Attempted to update non-existing product with SKU: %s", sku)
    return None

def delete_product(sku):
    """
    Delete a product from the product database by SKU.

    Args:
        sku (str): The SKU of the product to delete.

    Returns:
        bool: True if the product was successfully deleted, False otherwise.
    """
    if sku in products:
        del products[sku]
        logger.info("Product deleted with SKU: %s", sku)
        return True
    logger.warning("Attempted to delete non-existing product with SKU: %s", sku)
    return False

def get_all_products():
    """
    Retrieve all products from the product database.

    Returns:
        dict: A dictionary containing all products in the database.
    """
    return products

# End of data/product_db.py

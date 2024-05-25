"""
This module defines the Product class, which represents a product with methods to handle creation and updates.

The Product class has the following attributes:
- sku: A unique identifier for the product.
- name: The name of the product.
- description: The description of the product.
- price: The price of the product.
- stock: The stock level of the product.

The Product class provides the following methods:
- __init__(self, name, description, price, stock): Initializes a new product instance.
- create(cls, name, description, price, stock): Factory method to create a new product instance.
- update_stock(self, quantity): Updates the stock level for the product.
- update_price(self, new_price): Updates the price of the product.
- to_dict(self): Serializes the product to a dictionary.
"""

import uuid
from utility.logger import setup_logger

# Initialize the logger
logger = setup_logger('product_log')

class Product:
    """
    A class to represent a product with methods to handle creation and updates.
    """

    def __init__(self, name, description, price, stock):
        """
        Initializes a new product instance.

        Parameters:
        - name (str): The name of the product.
        - description (str): The description of the product.
        - price (float): The price of the product.
        - stock (int): The stock level of the product.
        """
        self.sku = str(uuid.uuid4())  # Generate a unique SKU
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        logger.debug("Product instance created with SKU: %s", self.sku)

    @classmethod
    def create(cls, name, description, price, stock):
        """
        Factory method to create a new product instance.

        Parameters:
        - name (str): The name of the product.
        - description (str): The description of the product.
        - price (float): The price of the product.
        - stock (int): The stock level of the product.

        Returns:
        - instance (Product): The newly created product instance.
        """
        instance = cls(name, description, price, stock)
        logger.debug("New Product created with SKU: %s", instance.sku)
        return instance

    def update_stock(self, quantity):
        """
        Updates the stock level for the product.

        Parameters:
        - quantity (int): The quantity to add or subtract from the stock level.

        Raises:
        - ValueError: If the resulting stock level would be negative.
        """
        if self.stock + quantity < 0:
            logger.error("Attempted to set negative stock for product SKU: %s", self.sku)
            raise ValueError("Stock cannot be negative.")
        self.stock += quantity
        logger.info("Stock updated for product SKU: %s, new stock level: %d", self.sku, self.stock)

    def update_price(self, new_price):
        """
        Updates the price of the product.

        Parameters:
        - new_price (float): The new price of the product.

        Raises:
        - ValueError: If the new price is negative.
        """
        if new_price < 0:
            logger.error("Attempted to set negative price for product SKU: %s", self.sku)
            raise ValueError("Price cannot be negative.")
        self.price = new_price
        logger.info("Price updated for product SKU: %s, new price: %.2f", self.sku, self.price)

    def to_dict(self):
        """
        Serializes the product to a dictionary.

        Returns:
        - dict: A dictionary representation of the product.
        """
        return {
            "sku": self.sku,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock
        }

# End of data/product.py

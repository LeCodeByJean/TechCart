"""
This module contains the API routes for the inventory management system.

The inventory management system allows users to create, retrieve, update, and
delete products in the inventory. The API routes are implemented using Flask
blueprints.

The following routes are available:
- POST /products: Create a new product in the inventory.
- GET /products: Retrieve all products in the inventory.
- GET /products/<sku>: Retrieve a product by its SKU.
- PUT /products/<sku>: Update a product by its SKU.
- DELETE /products/<sku>: Delete a product by its SKU.

The API routes are implemented using the following functions:
- create_product: Create a new product in the inventory.
- get_all_products_endpoint: Retrieve all products in the inventory.
- retrieve_product: Retrieve a product by its SKU.
- modify_product: Update a product by its SKU.
- remove_product: Delete a product by its SKU.

The API routes are registered with a Flask application instance in the
create_app function. The Flask application is run with the debug mode enabled
if the script is executed directly.

Attributes:
    inventory_api (Blueprint): Blueprint for the inventory API routes.
    logger (Logger): Logger instance for logging messages.
    app_instance (Flask): Flask application instance for the inventory API.
    limiter (Limiter): Rate limiter for API requests.

Safety focus:
    What: The rate limiter is used to limit the number of requests to the API.
    Why: To prevent abuse of the API and protect against denial-of-service attacks.
    How: The rate limiter works by limiting the number of requests from a single IP address.
"""
from flask import Blueprint, jsonify, request, Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from data.product_db import (
    add_product, get_product, update_product, delete_product, get_all_products
)
from utility.logger import setup_logger
from config import Config

# Initialize a blueprint for inventory routes
inventory_api = Blueprint('inventory_api', __name__)

# Initialize the logger
logger = setup_logger('inventory_api_log')

# Initialize the Limiter
limiter = Limiter(
    get_remote_address,
    app=None,  # We will attach it to the Flask app later
    default_limits=Config.RATE_LIMIT.split(';')
)

@inventory_api.route('/products', methods=['POST'])
@limiter.limit(Config.RATE_LIMIT)
def create_product():
    """
    Creates a new product in the inventory.

    Returns:
        JSON response with the created product data and a status code of 201.
        If the product data is missing or an error occurs, returns a JSON
        error message with a status code of 400.
    """
    data = request.get_json()
    try:
        result = add_product(data['name'], data['description'], data['price'], data['stock'])
        logger.info("Successfully created a new product with SKU: %s", result['sku'])
        return jsonify(result), 201
    except KeyError as e:
        logger.error("Failed to create product due to missing data: %s", str(e))
        return jsonify({'error': f'Missing product data: {e}'}), 400
    except Exception as e:
        logger.error("Error in creating product: %s", str(e))
        return jsonify({'error': str(e)}), 400

@inventory_api.route('/products', methods=['GET'])
@limiter.limit(Config.RATE_LIMIT)
def get_all_products_endpoint():
    """
    Retrieves all products in the inventory.

    Returns:
        JSON response with a list of all products and a status code of 200.
        If no products are found, returns a JSON error message with a
        status code of 404.
    """
    products = get_all_products()
    if products:
        product_list = [{"SKU": pid, **details} for pid, details in products.items()]
        return jsonify(product_list), 200
    else:
        return jsonify({'error': 'No product found in inventory'}), 404

@inventory_api.route('/products/<sku>', methods=['GET'])
@limiter.limit(Config.RATE_LIMIT)
def retrieve_product(sku):
    """
    Retrieves a product by its SKU.

    Parameters:
        sku (str): The SKU of the product to retrieve.

    Returns:
        JSON response with the product data and a status code of 200.
        If the product is not found, returns a JSON error message with a
        status code of 404.
    """
    product = get_product(sku)
    if product:
        logger.info("Product retrieved successfully for SKU: %s", sku)
        return jsonify(product), 200
    else:
        logger.warning("Product not found for SKU: %s", sku)
        return jsonify({'error': 'Product not found'}), 404

@inventory_api.route('/products/<sku>', methods=['PUT'])
@limiter.limit(Config.RATE_LIMIT)
def modify_product(sku):
    """
    Updates a product by its SKU.

    Parameters:
        sku (str): The SKU of the product to update.

    Returns:
        JSON response with the updated product data and a status code of 200.
        If the product is not found, returns a JSON error message with a
        status code of 404.
    """
    data = request.get_json()
    try:
        product = update_product(sku,
                                name=data.get('name'),
                                description=data.get('description'),
                                price=data.get('price'),
                                stock=data.get('stock'))
        if product:
            logger.info("Product updated successfully for SKU: %s", sku)
            return jsonify(product), 200
        else:
            logger.error("Product not found for update for SKU: %s", sku)
            return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        logger.error("Error updating product for SKU: %s: %s", sku, str(e))
        return jsonify({'error': str(e)}), 400

@inventory_api.route('/products/<sku>', methods=['DELETE'])
@limiter.limit(Config.RATE_LIMIT)
def remove_product(sku):
    """
    Deletes a product by its SKU.

    Parameters:
        sku (str): The SKU of the product to delete.

    Returns:
        JSON response with a success message and a status code of 200.
        If the product is not found, returns a JSON error message with a
        status code of 404.
    """
    if delete_product(sku):
        logger.info("Product deleted successfully with SKU: %s", sku)
        return jsonify({'message': 'Product deleted successfully'}), 200
    else:
        logger.warning("Attempted to delete non-existing product with SKU: %s", sku)
        return jsonify({'error': 'Product not found'}), 404

def create_app():
    """
    Creates a Flask application with the inventory API blueprint.

    Returns:
        Flask: A Flask application instance.
    """
    flask_app = Flask(__name__)
    flask_app.config.from_object(Config)
    setup_logger('flask_log')
    flask_app.register_blueprint(inventory_api, url_prefix='/api')
    limiter.init_app(flask_app)  # Attach the limiter to the app
    return flask_app

# Initialize the Flask application
app_instance = create_app()

if __name__ == '__main__':
    app_instance.run(debug=Config.DEBUG)

# End of API/inventory_api.py

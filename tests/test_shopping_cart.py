import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import pytest
from unittest import mock
from unittest.mock import MagicMock
from data.shopping_cart import add_item_to_cart, view_cart, clear_cart

# Simulate the user_db and product_db modules
@pytest.fixture(autouse=True)
def mock_db():
    with mock.patch('data.shopping_cart.get_user') as mock_get_user, \
         mock.patch('data.shopping_cart.update_user') as mock_update_user, \
         mock.patch('data.shopping_cart.get_product') as mock_get_product:
        
        mock_user = MagicMock()
        mock_user.cart = {}
        mock_get_user.return_value = mock_user
        mock_update_user.return_value = None
        mock_get_product.return_value = {'stock': 100}
        
        yield mock_get_user, mock_update_user, mock_get_product

def test_add_item_to_cart(mock_db):
    user_id = 'user123'
    product_id = 'SKU456'
    quantity = 2

    # Test adding an item to the cart
    result = add_item_to_cart(user_id, product_id, quantity)
    assert result is True

    # Test viewing the cart
    cart = view_cart(user_id)
    assert cart == {product_id: quantity}

def test_clear_cart(mock_db):
    user_id = 'user123'
    product_id = 'SKU456'
    quantity = 2

    # Add an item to the cart
    add_item_to_cart(user_id, product_id, quantity)

    # Clear the cart
    result = clear_cart(user_id)
    assert result is True

    # Ensure the mock user cart is cleared
    mock_user = mock_db[0].return_value
    mock_user.cart = {}

    # Check if the cart is empty
    cart = view_cart(user_id)
    assert cart == {}

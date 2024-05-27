import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest import mock
from services.payment_process import process_payment

@pytest.mark.parametrize("inputs, expected", [
    (["", "1234567890123456", "12", "25", "123"], "declined"),  # Missing cardholder name
    (["User", "123", "12", "25", "123"], "declined"),  # Invalid card number (less than 16 digits)
    (["User", "1234567890123456", "1", "24", "123"], "declined"),  # Invalid expiry month
    (["User", "1234567890123456", "12", "23", "123"], "declined"),  # Invalid expiry year
    (["User", "1234567890123456", "12", "25", "12"], "declined"),  # Invalid CVV
    (["User", "1234567890123456", "12", "28", "123"], "approved"),  # Valid input
])
def test_process_payment(inputs, expected):
    with mock.patch('builtins.input', side_effect=inputs):
        assert process_payment() == expected

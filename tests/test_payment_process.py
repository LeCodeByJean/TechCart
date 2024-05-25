import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest import mock
from services.payment_process import process_payment

@pytest.mark.parametrize("inputs, expected", [
    (["", "1234567812345678", "12", "25", "123"], "declined"),  # Missing cardholder name
    (["User name", "123456781234", "12", "25", "123"], "declined"),  # Invalid card number
    (["User name", "1234567812345678", "1", "25", "123"], "declined"),  # Invalid expiry month
    (["User name", "1234567812345678", "12", "5", "123"], "declined"),  # Invalid expiry year
    (["User name", "1234567812345678", "12", "25", "12"], "declined"),  # Invalid CVV
    (["User name", "1234567812345678", "12", "22", "123"], "declined"),  # Expired card
    (["User name", "1234567812345678", "12", "50", "123"], "approved"),  # Valid input
])
def test_process_payment(inputs, expected):
    with mock.patch('builtins.input', side_effect=inputs):
        assert process_payment() == expected

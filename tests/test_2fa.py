import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import logging
from utility.two_factor_auth import generate_security_code, send_security_code

def test_generate_security_code():
    code = generate_security_code()
    assert isinstance(code, str)
    assert len(code) == 6
    assert code.isdigit()

@pytest.fixture
def caplog_info_level(caplog):
    caplog.set_level(logging.DEBUG)  # Set to DEBUG level to capture all messages
    return caplog

def test_send_security_code(caplog_info_level):
    email = "test@example.com"
    code = generate_security_code()
    send_security_code(email, code)
    
    # Check if the log contains the correct information
    assert "Simulation of email with the 2FA code. Check logs/techcart.log to see the code." in caplog_info_level.text
    assert f"The 2FA code for {email} is: {code}" in caplog_info_level.text

if __name__ == "__main__":
    pytest.main()

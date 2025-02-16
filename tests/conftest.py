import pytest
import sys
import os

# Add the directory containing main.py to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock RPi.GPIO before any tests are collected
try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    from mock_gpio import GPIO
    sys.modules['RPi.GPIO'] = GPIO

@pytest.fixture(autouse=True)
def mock_gpio(monkeypatch):
    from mock_gpio import GPIO
    monkeypatch.setattr('RPi.GPIO', GPIO)

@pytest.fixture(autouse=True)
def mock_adafruit_mcp9808(monkeypatch):
    from mock_adafruit_mcp9808 import MCP9808
    monkeypatch.setattr('adafruit_mcp9808.MCP9808', MCP9808)

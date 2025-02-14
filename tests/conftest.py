import pytest

@pytest.fixture(autouse=True)
def mock_gpio(monkeypatch):
    from mock_gpio import GPIO
    monkeypatch.setattr('RPi.GPIO', GPIO)

@pytest.fixture(autouse=True)
def mock_adafruit_mcp9808(monkeypatch):
    from mock_adafruit_mcp9808 import MCP9808
    monkeypatch.setattr('adafruit_mcp9808.MCP9808', MCP9808)

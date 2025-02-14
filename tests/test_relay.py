import pytest
from unittest.mock import patch
import relay

@patch('relay.GPIO')
def test_setup(mock_gpio):
    relay.setup()
    mock_gpio.setwarnings.assert_called_with(False)
    mock_gpio.setmode.assert_called_with(mock_gpio.BCM)
    mock_gpio.setup.assert_any_call(relay.pin_light, mock_gpio.OUT, initial=mock_gpio.HIGH)

@patch('relay.GPIO')
def test_day_light(mock_gpio):
    relay.day_light()
    mock_gpio.output.assert_any_call(relay.pin_light, mock_gpio.LOW)
    mock_gpio.output.assert_any_call(relay.pin_uvb, mock_gpio.LOW)
    mock_gpio.output.assert_any_call(relay.pin_night, mock_gpio.HIGH)

@patch('relay.GPIO')
def test_night_light(mock_gpio):
    relay.night_light()
    mock_gpio.output.assert_any_call(relay.pin_light, mock_gpio.HIGH)
    mock_gpio.output.assert_any_call(relay.pin_uvb, mock_gpio.HIGH)
    mock_gpio.output.assert_any_call(relay.pin_night, mock_gpio.LOW)

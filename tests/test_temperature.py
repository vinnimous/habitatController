import pytest
import datetime
from unittest.mock import patch, MagicMock
import temperature

@patch('temperature.datetime')
@patch('temperature.mapSun')
def test_find_season(mock_mapSun, mock_datetime):
    mock_datetime.datetime.now.return_value = datetime.datetime(2023, 12, 25)
    temperature.find_season("day")
    assert temperature.season == "winter"

@patch('temperature.relay')
@patch('temperature.mapSun')
@patch('temperature.datetime')
def test_control_heat(mock_datetime, mock_mapSun, mock_relay):
    mock_datetime.datetime.now.return_value = datetime.datetime(2023, 12, 25, 12, 0)
    mock_mapSun.sunset = datetime.datetime(2023, 12, 25, 18, 0)
    temperature.cycle = "day"
    temperature.season = "winter"
    temperature.control_heat()
    assert temperature.temp_set == temperature.winter_day

@patch('temperature.busio.I2C')
@patch('temperature.adafruit_mcp9808.MCP9808')
def test_check_temp(mock_mcp9808, mock_i2c):
    mock_sensor = MagicMock()
    mock_sensor.temperature = 25.0
    mock_mcp9808.return_value = mock_sensor
    temperature.check_temp()
    assert temperature.t_hot == 77.0
    assert temperature.t_cold == 77.0

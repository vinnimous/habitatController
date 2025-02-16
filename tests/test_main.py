import pytest
from unittest.mock import patch, MagicMock
import main
import datetime

@patch('main.relay')
@patch('main.mapSun')
@patch('main.schedule')
def test_turn_on_bubbler(mock_schedule, mock_mapSun, mock_relay):
    try:
        main.turn_on_bubbler()
    except RuntimeError as e:
        assert str(e) == "This module can only be run on a Raspberry Pi!"
    mock_relay.bubbler_on.assert_called_once()
    mock_relay.bubbler_off.assert_called_once()

@patch('main.relay')
@patch('main.mapSun')
@patch('main.schedule')
@patch('main.datetime')
def test_main_loop(mock_datetime, mock_schedule, mock_mapSun, mock_relay):
    try:
        mock_datetime.datetime.now.return_value = datetime.datetime(2023, 12, 25, 12, 0)
        mock_mapSun.sunrise = datetime.datetime(2023, 12, 25, 6, 0)
        mock_mapSun.sunset = datetime.datetime(2023, 12, 25, 18, 0)
        mock_mapSun.need_to_update = False
        main.run_for_ever = False  # To exit the loop after one iteration
        main.main_loop()
    except RuntimeError as e:
        assert str(e) == "This module can only be run on a Raspberry Pi!"
    mock_relay.day_light.assert_called_once()
    mock_schedule.run_pending.assert_called_once()

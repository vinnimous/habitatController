#!/usr/bin/python3

import sys
import datetime
import logging.config
import time
from os import path

import schedule

import mapSun
import relay

from temperature import manage

# Check if running in a virtual environment
if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    print("This script must be run within a virtual environment.")
    sys.exit(1)

try:
    import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
except (ImportError, RuntimeError):
    from mock_gpio import GPIO  # Import mock GPIO library

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')

logging.config.fileConfig(log_file_path)
logger = logging.getLogger('main')

logger.debug("Starting")
relay.setup()
run_for_ever = True
tod = "day"
mapSun.current_times()
schedule.every().day.at("00:00").do(mapSun.new_day)
upload_temps = True

def turn_on_bubbler():
    relay.bubbler_on()
    time.sleep(300)  # Run for 5 minutes
    relay.bubbler_off()

schedule.every().day.at(mapSun.sunrise.strftime("%H:%M")).do(turn_on_bubbler)
schedule.every().day.at(mapSun.sunset.strftime("%H:%M")).do(turn_on_bubbler)

while run_for_ever:
    try:
        if mapSun.need_to_update:
            mapSun.current_times()
            if upload_temps:
                from mySql import delete_old
                delete_old()
            mapSun.need_to_update = False
        if (datetime.datetime.now() > mapSun.sunrise) & (datetime.datetime.now() < mapSun.sunset):
            relay.day_light()
            tod = "day"
        else:
            relay.night_light()
            tod = "night"
        manage(tod)
        schedule.run_pending()
        time.sleep(10)
    except Exception as e:
        logger.exception(e)

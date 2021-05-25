#!/usr/bin/python3

import datetime
import logging.config
import time
from os import path

import schedule

import mapSun
import relay
from temperature import manage

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

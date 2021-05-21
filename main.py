#!/usr/bin/python3

import datetime
import logging.config
import time

import schedule

from mapSun import current_times, need_to_update, new_day, sunrise, sunset
from mySql import delete_old
from relay import day_light, night_light, setup
from temperature import manage

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('main')

logger.debug("Starting")
setup()
run_for_ever = True
tod = "day"
current_times()
schedule.every().day.at("00:00").do(new_day)

log_upload = True

while run_for_ever:
    try:
        if need_to_update:
            current_times()
            if log_upload:
                delete_old()
            need_to_update = False
        if (datetime.datetime.now() > sunrise) & (datetime.datetime.now() < sunset):
            day_light()
            tod = "day"
        else:
            night_light()
            tod = "night"
        manage(tod)
        schedule.run_pending()
        time.sleep(10)
    except Exception as e:
        logger.exception(e)

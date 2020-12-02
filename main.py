#!/usr/bin/python3

import datetime
import logging
import logging.handlers as handlers
import time

import schedule

import errorMessages
import mapSun
import relay
import temperature

logger = logging.getLogger('habitatController')
logger.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logHandler = handlers.RotatingFileHandler('/tmp/habitatController.log', maxBytes=5242880, backupCount=2)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

relay.setup()
run_for_ever = True
tod = "day"
mapSun.current_times()
schedule.every().day.at("00:00").do(mapSun.new_day)

while run_for_ever:
    try:
        now = datetime.datetime.now()
        if mapSun.need_to_update:
            mapSun.current_times()
            mapSun.need_to_update = False
        if (now > mapSun.sunrise) & (now < mapSun.sunset):
            relay.day_light()
            relay.heater_on()
            tod = "day"
        else:
            relay.night_light()
            relay.heater_off()
            tod = "night"
        temperature.control_heat()
        schedule.run_pending()
        time.sleep(10)
    except:
        logger.error(errorMessages.E1)

#!/usr/bin/python3

import datetime
import time

import schedule

import errorMessages
import mapSun
import relay
import temperature
import mySql

relay.setup()
run_for_ever = True
tod = "day"
mapSun.current_times()
schedule.every().day.at("00:00").do(mapSun.new_day)

log_upload = True
log_std_out = False

while run_for_ever:
    try:
        if mapSun.need_to_update:
            mapSun.current_times()
            if log_upload:
                mySql.delete_old()
            mapSun.need_to_update = False
        if (datetime.datetime.now() > mapSun.sunrise) & (datetime.datetime.now() < mapSun.sunset):
            relay.day_light()
            tod = "day"
        else:
            relay.night_light()
            tod = "night"
        temperature.manage(tod)
        schedule.run_pending()
        time.sleep(10)
    except:
        print(errorMessages.E1)
#!/usr/bin/python3

import datetime
import time

import adafruit_mcp9808
import board
import busio
import schedule
import errorMessages
import mapSun
import relay
import temperature

relay.setup()
run_for_ever = True
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
        print(mapSun.sunset)
        temperature.control_heat(tod)
        schedule.run_pending()
        time.sleep(10)
    except:
        print(errorMessages.E1)

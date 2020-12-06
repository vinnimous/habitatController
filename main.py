#!/usr/bin/python3

import datetime
import time

import schedule

import errorMessages
import mapSun
import relay
import temperature

relay.setup()
run_for_ever = True
tod = "day"
mapSun.current_times()
schedule.every().day.at("00:00").do(mapSun.new_day)

while run_for_ever:
    try:
        if mapSun.need_to_update:
            mapSun.current_times()
            mapSun.need_to_update = False
        if (datetime.datetime.now() > mapSun.sunrise) & (datetime.datetime.now() < mapSun.sunset):
            print("here")
            relay.day_light()
            tod = "day"
        else:
            print("there")
            relay.night_light()
            tod = "night"
        print(tod)
        temperature.find_season(tod)
        print("got temp")
        schedule.run_pending()
        time.sleep(10)
    except:
        print(errorMessages.E1)
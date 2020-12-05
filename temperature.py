import datetime
import time

import adafruit_mcp9808
import board
import busio
import RPi.GPIO as GPIO

import errorMessages
import mapSun
import relay
import mySql

upload = False

h_hot = 0
h_cold = 0
t_hot = 0
t_cold = 0

heater_status = 0
uvb_status = 0
day_status = 0
night_status = 0

season = "unknown"

spring = "spring"
summer = "summer"
autumn = "autumn"
winter = "winter"

spring_day = 102
summer_day = 105
autumn_day = 102
winter_day = 100
spring_night = 79
summer_night = 80
autumn_night = 79
winter_night = 79
fail_safe = 75

spring_season = "03-01"
summer_season = "06-01"
autumn_season = "09-01"
winter_season = "12-01"

now = datetime.datetime.now()


def control_heat(tod):
    global season, now
    if (now.strftime("%m-%d")) > winter_season:
        season = winter
    elif (now.strftime("%m-%d")) > autumn_season:
        season = autumn
    elif (now.strftime("%m-%d")) > summer_season:
        season = summer
    elif (now.strftime("%m-%d")) > spring_season:
        season = spring
    else:
        season = winter
    if (tod == "day") & (season == winter):
        while now < mapSun.sunset:
            check_temp()
            if t_hot < fail_safe:
                relay.emergency_heat()
                temp_status(tod, winter_day)
            elif t_hot < winter_day:
                relay.heater_on()
                temp_status(tod, winter_day)
            elif t_hot < winter_day + 1:
                temp_status(tod, winter_day)
            else:
                relay.heater_off()
                temp_status(tod, winter_day)
            time.sleep(5)
    elif (tod == "day") & (season == autumn):
        while now < mapSun.sunset:
            control_heat(tod, autumn_day)
    elif (tod == "day") & (season == summer):
        while now < mapSun.sunset:
            control_heat(tod, summer_day)
    elif (tod == "day") & (season == spring):
        while now < mapSun.sunset:
            control_heat(tod, spring_day)
    elif (tod == "night") & (season == winter):
        while now > mapSun.sunset or now < mapSun.sunrise:
            control_heat(tod, winter_night)
    elif (tod == "night") & (season == autumn):
        while now > mapSun.sunset or now < mapSun.sunrise:
            control_heat(tod, autumn_night)
    elif (tod == "night") & (season == summer):
        while now > mapSun.sunset or now < mapSun.sunrise:
            control_heat(tod, summer_night)
    elif (tod == "night") & (season == spring):
        while now > mapSun.sunset or now < mapSun.sunrise:
            control_heat(tod, spring_night)


def control_heat(tod, temp_set):
    check_temp()
    if t_hot < fail_safe:
        relay.emergency_heat()
        temp_status(tod, temp_set)
    elif t_hot < temp_set:
        relay.heater_on()
        temp_status(tod, temp_set)
    elif t_hot < temp_set + 1:
        temp_status(tod, temp_set)
    else:
        relay.heater_off()
        temp_status(tod, temp_set)
    time.sleep(5)


def check_temp():
    global h_hot, t_hot, h_cold, t_cold
    try:
        t_hot = adafruit_mcp9808.MCP9808(busio.I2C(board.SCL, board.SDA)).temperature * 9 / 5 + 32
    except:
        print(errorMessages.E5)


def check_relays():
    global uvb_status, day_status, night_status, heater_status
    try:
        if GPIO.input(relay.pin_heater):
            heater_status = 0
        else:
            heater_status = 1
        if GPIO.input(relay.pin_light):
            day_status = 0
        else:
            day_status = 1
        if GPIO.input(relay.pin_uvb):
            uvb_status = 0
        else:
            uvb_status = 1
        if GPIO.input(relay.pin_night):
            night_status = 0
        else:
            night_status = 1
    except:
        print(errorMessages.E3)


def temp_status(tod, temp_set):
    if upload:
        check_relays()
        try:
            mySql.insert(now, tod, season, temp_set, t_hot, uvb_status, day_status,
                         night_status, heater_status)
        except:
            print((errorMessages.E7))

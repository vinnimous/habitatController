import datetime
import time

import adafruit_mcp9808
import board
import busio
import RPi.GPIO as GPIO

import errorMessages
import mapSun
import relay

h_hot = 0
h_cold = 0
t_hot = 0
t_cold = 0

heater_status = "off"
season = "unknown"

spring = "spring"
summer = "summer"
autumn = "autumn"
winter = "winter"

spring_day = 99
summer_day = 103
autumn_day = 99
winter_day = 98
spring_night = 79
summer_night = 80
autumn_night = 79
winter_night = 78

spring_season = "03-01"
summer_season = "06-01"
autumn_season = "09-01"
winter_season = "12-01"


def control_heat(tod):
    global season
    if (datetime.datetime.now().strftime("%m-%d")) > winter_season:
        season = winter
    elif (datetime.datetime.now().strftime("%m-%d")) > autumn_season:
        season = autumn
    elif (datetime.datetime.now().strftime("%m-%d")) > summer_season:
        season = summer
    elif (datetime.datetime.now().strftime("%m-%d")) > spring_season:
        season = spring
    else:
        season = winter
    print("Season: {} TimeOfDay: {}".format(season, tod))
    if (tod == "day") & (season == winter):
        while datetime.datetime.now() < mapSun.sunset:
            check_temp()
            if t_hot < winter_day:
                relay.heater_on()
                temp_status()
            else:
                relay.heater_off()
                temp_status()
            time.sleep(2)
    elif (tod == "day") & (season == autumn):
        while datetime.datetime.now() < mapSun.sunset:
            check_temp()
            if t_hot < autumn_day:
                relay.heater_on()
                temp_status()
            else:
                relay.heater_off()
                temp_status()
            time.sleep(2)
    elif (tod == "day") & (season == summer):
        while datetime.datetime.now() < mapSun.sunset:
            check_temp()
            if t_hot < summer_day:
                relay.heater_on()
                temp_status()
            else:
                relay.heater_off()
                temp_status()
            time.sleep(2)
    elif (tod == "day") & (season == spring):
        while datetime.datetime.now() < mapSun.sunset:
            check_temp()
            if t_hot < spring_day:
                relay.heater_on()
                temp_status()
            else:
                relay.heater_off()
                temp_status()
            time.sleep(2)
    elif (tod == "night") & (season == winter):
        while datetime.datetime.now() > mapSun.sunset | datetime.datetime.now() < mapSun.sunrise:
            check_temp()
            if t_hot < winter_night:
                relay.heater_on()
                temp_status()
            else:
                relay.heater_off()
                temp_status()
            time.sleep(2)
    elif (tod == "night") & (season == autumn):
        while datetime.datetime.now() > mapSun.sunset | datetime.datetime.now() < mapSun.sunrise:
            check_temp()
            if t_hot < autumn_night:
                relay.heater_on()
                temp_status()
            else:
                relay.heater_off()
                temp_status()
            time.sleep(2)
    elif (tod == "night") & (season == summer):
        while datetime.datetime.now() > mapSun.sunset | datetime.datetime.now() < mapSun.sunrise:
            check_temp()
            if t_hot < summer_night:
                relay.heater_on()
                temp_status()
            else:
                relay.heater_off()
                temp_status()
            time.sleep(2)
    elif (tod == "night") & (season == spring):
        while datetime.datetime.now() > mapSun.sunset | datetime.datetime.now() < mapSun.sunrise:
            check_temp()
            if t_hot < spring_night:
                relay.heater_on()
                temp_status()
            else:
                relay.heater_off()
                temp_status()
            time.sleep(2)


def check_temp():
    global h_hot, t_hot, h_cold, t_cold
    try:
        t_hot = adafruit_mcp9808.MCP9808(busio.I2C(board.SCL, board.SDA)).temperature * 9 / 5 + 32
    except:
        print(errorMessages.E5)


def check_heater_relay():
    global heater_status
    try:
        if GPIO.input(relay.pin_heater):
            heater_status = "on"
        else:
            heater_status = "off"
    except:
        print(errorMessages.E3)


def temp_status(tod):
    check_heater_relay()
    print("Season: {} TimeOfDay: {} Temp: {} Heater {}".format(season, tod, t_hot, heater_status))

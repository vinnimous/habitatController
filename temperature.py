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
std_out = True

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

cycle = "unknown"

spring_day = 102
summer_day = 105
autumn_day = 102
winter_day = 100
spring_night = 79
summer_night = 80
autumn_night = 79
winter_night = 79
fail_safe = 75
temp_set = fail_safe

spring_season = "03-01"
summer_season = "06-01"
autumn_season = "09-01"
winter_season = "12-01"


def manage(tod):
    find_season(tod)
    control_heat()


def find_season(tod):
    global season, cycle
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
    cycle = tod


def control_heat():
    global temp_set
    while (datetime.datetime.now() < mapSun.sunset) and (cycle == "day") and (season == winter):
        temp_set = winter_day
        control_elements()
        break
    while (datetime.datetime.now() < mapSun.sunset) and (cycle == "day") and (season == autumn):
        temp_set = autumn_day
        control_elements()
        break
    while (datetime.datetime.now() < mapSun.sunset) and (cycle == "day") and (season == summer):
        temp_set = summer_day
        control_elements()
        break
    while (datetime.datetime.now() < mapSun.sunset) and (cycle == "day") and (season == spring):
        temp_set = spring_day
        control_elements()
        break
    while ((datetime.datetime.now() > mapSun.sunset) or (datetime.datetime.now() < mapSun.sunrise)) \
            and (cycle == "night") and (season == winter):
        temp_set = winter_night
        control_elements()
        break
    while ((datetime.datetime.now() > mapSun.sunset) or (datetime.datetime.now() < mapSun.sunrise)) \
            and (cycle == "night") and (season == autumn):
        temp_set = autumn_night
        control_elements()
        break
    while ((datetime.datetime.now() > mapSun.sunset) or (datetime.datetime.now() < mapSun.sunrise)) \
            and (cycle == "night") and (season == summer):
        temp_set = summer_night
        control_elements()
        break
    while ((datetime.datetime.now() > mapSun.sunset) or (datetime.datetime.now() < mapSun.sunrise)) \
            and (cycle == "night") and (season == spring):
        temp_set = spring_night
        control_elements()
        break


def control_elements():
    check_temp()
    if t_hot < fail_safe or t_hot < temp_set - 5:
        relay.emergency_heat()
        temp_status()
    elif t_hot < temp_set:
        relay.heater_on()
        temp_status()
    elif t_hot < temp_set + 1:
        temp_status()
    else:
        relay.heater_off()
        temp_status()
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


def temp_status():
    if upload:
        try:
            check_relays()
            mySql.insert(datetime.datetime.now(), cycle, season, temp_set, t_hot, uvb_status, day_status,
                         night_status, heater_status)
        except:
            print(errorMessages.E7)
    if std_out:
        print("Current time: {} Cycle: {} Season: {} Temp_Set {} Temp_Read {} UVB {} Day {} Night {} Heat {}  ".
              format(datetime.datetime.now(), cycle, season, temp_set, t_hot, uvb_status, day_status,
                     night_status, heater_status))

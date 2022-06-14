import datetime
import logging
import time

import RPi.GPIO as GPIO
import adafruit_mcp9808
import board
import busio

import mapSun
import relay

logger = logging.getLogger('temperature')

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

spring_day = 98
summer_day = 100
autumn_day = 97
winter_day = 95
spring_night = 74
summer_night = 75
autumn_night = 73
winter_night = 72
fail_safe = 65
temp_set = fail_safe
temp_rest = 5
rest_count = 0
rest_limit = 12

spring_season = "03-01"
summer_season = "06-01"
autumn_season = "09-01"
winter_season = "12-01"


def manage(tod):
    find_season(tod)
    control_heat()


def find_season(tod):
    global season, cycle
    date_now = datetime.datetime.now().strftime("%m-%d")
    if date_now > winter_season:
        season = winter
    elif date_now > autumn_season:
        season = autumn
    elif date_now > summer_season:
        season = summer
    elif date_now > spring_season:
        season = spring
    else:
        season = winter
    cycle = tod
    logger.debug("Season: {} ".format(season))


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


def temp_gradiant():
    temp_diff = summer_day - summer_night
    time_diff = mapSun.noon - datetime.datetime.now()


def control_elements():
    global rest_count
    check_temp()
    if datetime.datetime.now() > mapSun.noon:
        if t_hot < fail_safe or t_hot < temp_set - 5:
            relay.emergency_heat()
    elif t_hot < temp_set:
        relay.heater_on()
    elif t_hot > temp_set:
        relay.heater_off()
    else:
        relay.heater_off()
    temp_status()
    time.sleep(temp_rest)


def check_temp():
    global h_hot, t_hot, h_cold, t_cold
    try:
        t_hot = (adafruit_mcp9808.MCP9808(busio.I2C(board.SCL, board.SDA)).temperature * (9 / 5)) + 32
    except Exception as e:
        logger.error("Failed to detect temperature: {}".format(e))


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
    except Exception as e:
        logger.error("Failed to control relays: {}".format(e))


def temp_status():
    from main import upload_temps
    if upload_temps:
        from mySql import insert
        try:
            insert(datetime.datetime.now(), cycle, season, temp_set, t_hot, uvb_status, day_status,
                   night_status, heater_status)
        except Exception as e:
            logger.error("Failed to insert temperature data: {}".format(e))
    logger.debug("Current time: {} Cycle: {} Season: {} Temp_Set {} Temp_Read {} UVB {} Day {} Night {} Heat {}  ".
                 format(datetime.datetime.now(), cycle, season, temp_set, t_hot, uvb_status, day_status,
                        night_status, heater_status))

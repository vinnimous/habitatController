import datetime
import time
import errorMessages
import mapSun
import relay
import busio
import adafruit_mcp9808
import board


i2c_bus = busio.I2C(board.SCL, board.SDA)
mcp = adafruit_mcp9808.MCP9808(i2c_bus)



h_hot = 0
h_cold = 0
t_hot = 0
t_cold = 0

spring = "spring"
summer = "summer"
autumn = "autumn"
winter = "winter"

spring_day = 99
summer_day = 102
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


def check_temp():
    global h_hot, t_hot, h_cold, t_cold
    t_hot = mcp.temperature * 9 / 5 + 32
    # if h_hot is not None and t_hot is not None:
    #     print("Temp={0:0.1f}*F  Humidity={1:0.1f}%".format(t_hot, h_hot))
    # else:
    #     print(errorMessages.E5)
    # if h_cold is not None and t_cold is not None:
    #     print("Temp={0:0.1f}*F  Humidity={1:0.1f}%".format(t_cold, h_cold))
    # else:
    #     print(errorMessages.E6)



def control_heat(tod):
    if (datetime.datetime.now().strftime("%m-%d")) > winter_season:
        season = winter
    elif (datetime.datetime.now().strftime("%m-%d")) > autumn_season:
        season = autumn_day
    elif (datetime.datetime.now().strftime("%m-%d")) > summer_season:
        season = summer
    elif (datetime.datetime.now().strftime("%m-%d")) > spring_season:
        season = spring
    else:
        season = winter

    if (tod == "day") & (season == winter):
        while datetime.datetime.now() < mapSun.sunset:
            check_temp()
            if t_hot < winter_day:
                relay.heater_on()
                temp_status(tod, season, t_hot, "On")
            else:
                relay.heater_off()
                temp_status(tod, season, t_hot, "Off")
            time.sleep(2)
    elif (tod == "day") & (season == autumn):
        while datetime.datetime.now() < mapSun.sunset:
            check_temp()
            if t_hot < autumn_day:
                relay.heater_on()
                temp_status(tod, season, t_hot, "On")
            else:
                relay.heater_off()
                temp_status(tod, season, t_hot, "Off")
            time.sleep(2)
    elif (tod == "day") & (season == summer):
        while datetime.datetime.now() < mapSun.sunset:
            check_temp()
            if t_hot < summer_day:
                relay.heater_on()
                temp_status(tod, season, t_hot, "On")
            else:
                relay.heater_off()
                temp_status(tod, season, t_hot, "Off")
            time.sleep(2)
    elif (tod == "day") & (season == spring):
        while datetime.datetime.now() < mapSun.sunset:
            check_temp()
            if t_hot < spring_day:
                relay.heater_on()
                temp_status(tod, season, t_hot, "On")
            else:
                relay.heater_off()
                temp_status(tod, season, t_hot, "Off")
            time.sleep(2)

def temp_status(tod, season, t_hot, relay):
    print("Season: " + season + " TimeOfDay: " + tod + " Temp: " + t_hot + "Heater: " + relay)

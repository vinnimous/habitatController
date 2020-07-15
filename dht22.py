import datetime
import time
import Adafruit_DHT
import errorMessages
import mapSun
import relay

hotSensor = Adafruit_DHT.DHT22
hotPin = 4

coldSensor = Adafruit_DHT.DHT22
coldPin = 6

h_hot = 0
h_cold = 0
t_hot = 0
t_cold = 0

spring_day = 98
summer_day = 101
autum_day = 98
winter_day = 95
spring_night = 78
summer_night = 80
autum_night = 78
winter_night = 75

spring_season = "03-01"
summer_season = "06-01"
autum_season = "09-01"
winter_season = "12-01"

def check_temp():
    global h_hot, t_hot, h_cold, t_cold
    h_hot, t_hot = Adafruit_DHT.read_retry(hotSensor, hotPin)
    t_hot = t_hot * 9 / 5.0 + 32  # Convert to Fahrenheit
    h_cold, t_cold = Adafruit_DHT.read_retry(coldSensor, coldPin)
    t_cold = t_cold * 9 / 5.0 + 32  # Convert to Fahrenheit
    if h_hot is not None and t_hot is not None:
        print("Temp={0:0.1f}*F  Humidity={1:0.1f}%".format(t_hot, h_hot))
    else:
        print(errorMessages.E5)
    if h_cold is not None and t_cold is not None:
        print("Temp={0:0.1f}*F  Humidity={1:0.1f}%".format(t_cold, h_cold))
    else:
        print(errorMessages.E6)

def control_heat(tod):
    if (datetime.datetime.now().strftime("%m-%d")) > winter_season:
        season = "winter"
    elif (datetime.datetime.now().strftime("%m-%d")) > autum_season:
        season = "autum"
    elif (datetime.datetime.now().strftime("%m-%d")) > summer_season:
        season = "summer"
    elif (datetime.datetime.now().strftime("%m-%d")) > spring_season:
        season = "spring"
    else:
        season = "winter"

    if (tod == "day") & (season == "winter"):
        while datetime.datetime.now() < mapSun.sunset:
            check_temp()
            if t_hot < winter_day:
                relay.heater_on()
            else:
                relay.heater_off()
            time.sleep(5)
    elif (tod == "day") & (season == "autum"):
        while datetime.datetime.now() < mapSun.sunset:
            check_temp()
            if t_hot < autum_day:
                relay.heater_on()
            else:
                relay.heater_off()
            time.sleep(5)
    elif (tod == "day") & (season == "summer"):
        while datetime.datetime.now() < mapSun.sunset:
            check_temp()
            if t_hot < summer_day:
                relay.heater_on()
            else:
                relay.heater_off()
            time.sleep(5)
    elif (tod == "day") & (season == "spring"):
        while datetime.datetime.now() < mapSun.sunset:
            check_temp()
            if t_hot < spring_day:
                relay.heater_on()
            else:
                relay.heater_off()
            time.sleep(5)
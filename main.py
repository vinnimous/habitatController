import datetime
import time
import schedule
import dht22
import errorMessages
import mapSun
import relay

relay.setup()
mapSun.current_times()
schedule.every().day.at("00:00").do(mapSun.new_day)

while True:
    try:
        now = datetime.datetime.now()
        if mapSun.need_to_update:
            mapSun.current_times()
            mapSun.need_to_update = False
        if (now > mapSun.sunrise) & (now < mapSun.sunset):
            relay.pin_light()
            relay.heater_on()
            tod = "day"
        elif now > mapSun.sunset:
            relay.pin_night()
            relay.heater_off()
            tod = "night"
        else:
            print(errorMessages.E4)
        # dht22.control_heat(tod)
        schedule.run_pending()
        time.sleep(10)
    except:
        print(errorMessages.E1)

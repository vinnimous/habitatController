import relay
import errorMessages
import datetime
import mapSun
import schedule
import time
import dht22

relay.setup()
mapSun.current_times()
schedule.every().day.at("00:00").do(mapSun.new_day)

while True:
    try:
        now = datetime.datetime.now()
        if mapSun.need_to_update:
            mapSun.current_times()
            mapSun.need_to_update = False
        if now > mapSun.sunrise:
            relay.dayLight()
            tod = "day"
        elif now > mapSun.sunset:
            relay.nightLight()
            tod = "night"
        else:
            print(errorMessages.E4)
        dht22.control_heat(tod)
        schedule.run_pending()
        time.sleep(10)
    except:
        print(errorMessages.E1)
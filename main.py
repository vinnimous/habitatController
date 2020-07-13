import relay
import errorMessages
import datetime
import mapSun
import schedule
import time

relay.setup()
dawn, sunrise, noon, sunset, dusk = mapSun.current_times()
schedule.every().day.at("00:00").do(mapSun.new_day)
while True:
    try:
        if mapSun.need_to_update:
            dawn, sunrise, noon, sunset, dusk = mapSun.current_times()
            mapSun.need_to_update = False
        else:
            dawn = dawn
            sunrise = sunrise
            noon = noon
            sunset = sunset
            dusk = dusk
        now = datetime.datetime.now()
        if now > sunrise:
            relay.dayLight()
        elif now > sunset:
            relay.nightLight()
        else:
            print(errorMessages.E4)
        time.sleep(10)
    except:
        print(errorMessages.E1)
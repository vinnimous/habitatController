import datetime
import time
import mapSun

import schedule
from astral.sun import sun
from astral import LocationInfo

dawn, sunrise, noon, sunset, dusk = mapSun.current_times()
print("START")
schedule.every(.5).minutes.do(mapSun.newDay)

while True:
    print("In Loop")
    print(mapSun.need_to_update)
    if mapSun.need_to_update:
        dawn, sunrise, noon, sunset, dusk = mapSun.current_times()
        mapSun.need_to_update = False
        print("Updated")
    else:
        print("Using Stored")
        dawn = dawn
        sunrise = sunrise
        noon = noon
        sunset = sunset
        dusk = dusk
    # schedule.every().day.at("00:55").do(test())
    schedule.run_pending()
    print("Resting")
    time.sleep(15)

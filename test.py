import datetime

import mapSun

mapSun.current_times()
next_event = mapSun.sunrise
current_event = mapSun.sunset
diff = current_event-next_event
sofar = 100-((next_event - datetime.datetime.now())/diff)*100
print("Dawn: %s, Sunrise: %s, Noon: %s, Sunset: %s, Dusk: %s" % (mapSun.dawn, mapSun.sunrise, mapSun.noon, mapSun.sunset, mapSun.dusk))

print("Now:\t\t %s \nNoon:\t\t %s \nSunrise:\t %s" %(datetime.datetime.now(), mapSun.noon, mapSun.sunrise))
print("Difference:\t %s" %(diff))

print("So far: \t%s" %(sofar))
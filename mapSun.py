import datetime
from astral.sun import sun
from astral import LocationInfo

need_to_update = True

def new_day():
    global need_to_update
    need_to_update = True

def current_times():
    city = LocationInfo("Clayton", "North Carolina", "US/Eastern", 35.650711, -78.4563914)
    s = sun(city.observer, datetime.datetime.now(), tzinfo=city.timezone)
    dawn = s["dawn"].replace(tzinfo=None)
    sunrise = s["sunrise"].replace(tzinfo=None)
    noon = s["noon"].replace(tzinfo=None)
    sunset = s["sunset"].replace(tzinfo=None)
    dusk = s["dusk"].replace(tzinfo=None)
    return dawn, sunrise, noon, sunset, dusk;
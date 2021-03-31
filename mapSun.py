import datetime

from astral import LocationInfo
from astral.sun import sun

from main import logger

need_to_update = True
dawn = 0
sunrise = 0
noon = 0
sunset = 0
dusk = 0


def new_day():
    global need_to_update
    need_to_update = True


def current_times():
    city = LocationInfo("Clayton", "North Carolina", "US/Eastern", 35.650711, -78.4563914)
    s = sun(city.observer, datetime.datetime.now(), tzinfo=city.timezone)
    global dawn, sunrise, noon, sunset, dusk
    dawn = s["dawn"].replace(tzinfo=None)
    sunrise = s["sunrise"].replace(tzinfo=None)
    noon = s["noon"].replace(tzinfo=None)
    sunset = s["sunset"].replace(tzinfo=None)
    dusk = s["dusk"].replace(tzinfo=None)
    logger.debug("Dawn: {} Sunrise: {} Sunset: {} Dusk: {}".format(dawn, sunrise, sunset, dusk))

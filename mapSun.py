import datetime
import logging
from configparser import ConfigParser
from os import path

from astral import LocationInfo
from astral.sun import sun

logger = logging.getLogger('mapSun')

need_to_update = True
dawn = 0
sunrise = 0
noon = 0
sunset = 0
dusk = 0

configs = "config.ini"
section = "location"


def new_day():
    global need_to_update
    need_to_update = True


def current_times():
    geoloc = LocationInfo()
    geoloc.name = read_configs().name
    geoloc.region = read_configs().region
    geoloc.timezone = read_configs().timezone
    geoloc.latitude = read_configs().latitude
    geoloc.longitude = read_configs().longitude
    s = sun(geoloc.observer, datetime.datetime.now(), tzinfo=geoloc.timezone)
    global dawn, sunrise, noon, sunset, dusk
    dawn = s["dawn"].replace(tzinfo=None)
    sunrise = s["sunrise"].replace(tzinfo=None)
    noon = s["noon"].replace(tzinfo=None)
    sunset = s["sunset"].replace(tzinfo=None)
    dusk = s["dusk"].replace(tzinfo=None)
    logger.debug("Dawn: {} Sunrise: {} Sunset: {} Dusk: {}".format(dawn, sunrise, sunset, dusk))


def read_configs():
    parser = ConfigParser()
    parser.read(path.join(path.dirname(path.abspath(__file__)), configs))
    if parser.has_section(section):
        name = parser.get(section, "name")
        region = parser.get(section, "region")
        timezone = parser.get(section, "timezone")
        latitude = parser.get(section, "latitude")
        longitude = parser.get(section, "longitude")
    else:
        raise Exception('{0} not found in the {1} file'.format(section, configs))
    return Loc(name, region, timezone, latitude, longitude)


class Loc:
    def __init__(self, name, region, timezone, latitude, longitude):
        self.name = name
        self.region = region
        self.timezone = timezone
        self.latitude = latitude
        self.longitude = longitude
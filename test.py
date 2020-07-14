import datetime
import sched
import time
import mapSun

import schedule
from astral.sun import sun
from astral import LocationInfo

mapSun.current_times()
print("START")
i=0
while True:
    print("In Loop")
    now = datetime.datetime.now()
    now = now + datetime.timedelta(days=180)
    spring_season = "03-01"
    summer_season = "06-01"
    autum_season = "09-01"
    winter_season = "12-01"
    if(now.strftime("%m-%d"))>winter_season:
        print("Winter")
    elif(now.strftime("%m-%d"))>autum_season:
        print("autum!!")
    elif(now.strftime("%m-%d"))>summer_season:
        print("SUMMER!!!")
    elif(now.strftime("%m-%d"))>spring_season:
        print("Spring")
    else:
        print("defaulting to winter")
    print("Resting")
    time.sleep(3)

import datetime
import time
import mapSun

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
        print("Autum")
    elif(now.strftime("%m-%d"))>summer_season:
        print("Summer")
    elif(now.strftime("%m-%d"))>spring_season:
        print("Spring")
    else:
        print("defaulting to winter")
    print("Resting")
    time.sleep(3)

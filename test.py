import datetime
import time

cycle = "night"
season = "winter"
temp_set = 78
t_hot = 79
heater_status = 1
uvb_status = 0
day_status = 0
night_status = 1

while True:
    print("Current time: {} Cycle: {} Season: {} Temp_Set {} Temp_Read {} UVB {} Day {} Night {} Heat {}  ".
          format(datetime.datetime.now(), cycle, season, temp_set, t_hot, uvb_status, day_status,
                 night_status, heater_status))
    time.sleep(5)

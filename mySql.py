import pymysql

sqlHost = "localhost"
sqlUser = "grafanauser"
sqlPass = "grafanauserPW"
sqlDB = "habitatHistoryDB"


def insert(date, tod, season, temp_set, temp_act, light_uvb, light_day, light_night, heat_bulb):
    db = pymysql.connect(sqlHost, sqlUser, sqlPass, sqlDB)
    cursor = db.cursor()
    sql = "INSERT INTO habitatHistoryTable ( \
        DATE, \
        TOD, \
        SEASON, \
        TEMP_SET, \
        TEMP_ACT, \
        LIGHT_UVB, \
        LIGHT_DAY, \
        LIGHT_NIGHT, \
        HEAT_BULB \
    ) VALUES ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
          (date, tod, season, temp_set, temp_act, light_uvb, light_day, light_night, heat_bulb)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()

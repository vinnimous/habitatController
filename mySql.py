import pymysql
import temperature

sqlHost = "localhost"
sqlUser = "grafanauser"
sqlPass = "grafanauserPW"
sqlDB = "habitatHistoryDB"
sqlArchiveLimit = 30


def insert(date, tod, season, temp_set, temp_act, light_uvb, light_day, light_night, heat_bulb):
    temperature.check_relays()
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


def delete_old():
    db = pymysql.connect(sqlHost, sqlUser, sqlPass, sqlDB)
    cursor = db.cursor()
    sql = "DELETE FROM from habitatHistoryTable where DATE < now() - interval %s DAY,"
    adr = (sqlArchiveLimit,)
    try:
        cursor.execute(sql, adr)
        db.commit()
    except:
        db.rollback()
    db.close()

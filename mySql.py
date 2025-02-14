import logging
from configparser import ConfigParser
from os import path

import pymysql

from temperature import check_relays

logger = logging.getLogger('mySql')
sqlArchiveLimit = 30


def read_db_config(filename='config.ini', section='mysql'):
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(path.join(path.dirname(path.abspath(__file__)), filename))

    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return db


def insert(date, tod, season, temp_set, temp_act_h, temp_act_c, light_uvb, light_day, light_night, heat_bulb):
    check_relays()
    db_config = read_db_config()
    db = pymysql.connect(**db_config)
    cursor = db.cursor()
    sql = "INSERT INTO habitatHistoryTable ( \
        DATE, \
        TOD, \
        SEASON, \
        TEMP_SET, \
        TEMP_ACT_H, \
        TEMP_ACT_C, \
        LIGHT_UVB, \
        LIGHT_DAY, \
        LIGHT_NIGHT, \
        HEAT_BULB \
    ) VALUES ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
          (date, tod, season, temp_set, temp_act_h, temp_act_c, light_uvb, light_day, light_night, heat_bulb)
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        logger.error("Failed to insert record from table: {}".format(e))
        db.rollback()
    finally:
        cursor.close()
        db.close()


def delete_old():
    db_config = read_db_config()
    db = pymysql.connect(**db_config)
    cursor = db.cursor()
    del_stmt = "DELETE FROM habitatHistoryTable WHERE DATE < NOW() - interval %s DAY;"
    find_old = "SELECT * FROM habitatHistoryTable WHERE DATE < NOW() - interval %s DAY;"
    adr = (sqlArchiveLimit,)
    try:
        cursor.execute(find_old, adr)
        records = cursor.fetchall()
        if len(records) > 0:
            cursor.execute(del_stmt, adr)
            db.commit()
            logger.debug(cursor.rowcount, " records deleted")
        else:
            logger.debug("No old records exsist")
    except Exception as e:
        logger.error("Failed to delete record from table: {}".format(e))
        db.rollback()
    finally:
        cursor.close()
        db.close()

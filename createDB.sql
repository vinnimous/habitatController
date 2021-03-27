CREATE DATABASE IF NOT EXISTS habitatHistoryDB;

create user 'grafanauser'@'localhost' identified by 'grafanauserPW';

grant all privileges on habitatHistoryDB.* to 'grafanauser'@'localhost';

flush privileges;

USE habitatHistoryDB;

CREATE TABLE IF NOT EXISTS habitatHistoryTable (
    DATE DATETIME,
    TOD VARCHAR(10),
    SEASON VARCHAR(15),
    TEMP_SET FLOAT,
    TEMP_ACT FLOAT,
    LIGHT_UVB BINARY,
    LIGHT_DAY BINARY,
    LIGHT_NIGHT BINARY,
    HEAT_BULB BINARY
);
#!/bin/bash

sudo apt-get install -y build-essential python-dev python-smbus python3-pip python-mysqldb
#https://grafana.com/docs/grafana/latest/installation/debian/
sudo apt-get install -y apt-transport-https software-properties-common wget mariadb-server

sudo apt-get install -y adduser libfontconfig1
wget https://dl.grafana.com/oss/release/grafana-rpi_7.3.4_armhf.deb
sudo dpkg -i grafana-rpi_7.3.4_armhf.deb



wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
sudo apt-get update
sudo apt-get install -y grafana
sudo service grafana-server start
sudo service grafana-server status
sudo update-rc.d grafana-server defaults

sudo mysql_secure_installation
sudo mysql -u root -p


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

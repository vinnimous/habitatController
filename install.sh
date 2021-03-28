#!/bin/bash

RASP_MOD_A="Raspberry Pi Model A"
RASP_MOD_B="Raspberry Pi Model B"
MODEL_FILE=/sys/firmware/devicetree/base/model
IS_TYPE_A=false
IS_TYPE_B=false
ERROR_MOD_NOT_FOUND="Undetected Raspberry Pi Model"
CRONJOB="@reboot python3 /home/pi/habitatController/main.py"
CRONFILE="/var/spool/cron/crontabs/pi"
CRONCAT="sudo cat $CRONFILE"
TMPFILE=/tmp/tmpCronJobs.txt
GRAFANA_ENABLE="sudo /bin/systemctl enable grafana-server"
GRAFANA_START="sudo /bin/systemctl start grafana-server"
GRAFANA_ENABLED="Loaded: loaded (/lib/systemd/system/grafana-server.service; enabled"
GRAFANA_RUNNING="Active: active (running)"
IS_GRAFANA_ENABLED=false
IS_GRAFANA_RUNNING=false

get_arch() {
  if grep -q "$RASP_MOD_A" "$MODEL_FILE"; then
    echo "Model A detected"
    IS_TYPE_A=true
  elif grep -q "$RASP_MOD_B" "$MODEL_FILE"; then
    echo "Model B detected"
    IS_TYPE_B=true
  else
    echo "Undetected Raspberry Pi Model"
  fi
}

updating() {
  sudo apt-get update -y
}

install_requirements() {
  pip3 install -r requirements.txt
}

install_basics() {
  sudo apt-get install -y build-essential python-dev python-smbus python3-pip
}

install_mysql() {
  sudo apt-get install -y apt-transport-https software-properties-common wget mariadb-server adduser libfontconfig1
  sudo apt-get install -y python-mysqldb
}

install_grafana() {
  if $RASP_MOD_B; then
    grafana_apt
  elif $RASP_MOD_A; then
    grafana_deb
  else
    echo "$ERROR_MOD_NOT_FOUND"
  fi
}

grafana_deb() {
  wget https://dl.grafana.com/oss/release/grafana-rpi_7.3.4_armhf.deb
  sudo dpkg -i grafana-rpi_7.3.4_armhf.deb
  #https://grafana.com/docs/grafana/latest/installation/debian/
}

grafana_apt() {
  wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
  echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
  sudo apt-get update
  sudo apt-get install -y grafana
}

start_grafana() {
  if $RASP_MOD_B; then
    sudo /bin/systemctl enable grafana-server
    sudo /bin/systemctl start grafana-server &
  elif $RASP_MOD_A; then
    sudo service grafana-server start
    sudo update-rc.d grafana-server defaults
  else
    echo "$ERROR_MOD_NOT_FOUND"
  fi
}

#check_grafana() {
#  if grep -q $GRAFANA_ENABLED "$MODEL_FILE"; then
#    echo "Model A detected"
#    IS_TYPE_A=true
#  elif grep -q $RASP_MOD_B "$MODEL_FILE"; then
#    echo "Model B detected"
#    IS_TYPE_B=true
#  else
#    echo "Undetected Raspberry Pi Model"
#  fi
#}

setup_mysql() {
  sudo mysql_secure_installation
  sudo mysql -u root -p <createDB.sql
}

create_cron() {
  crontab -l >$TMPFILE
  echo "$CRONJOB" >>$TMPFILE
  cron $TMPFILE
  rm $TMPFILE
  #echo "$CRONJOB" | sudo tee -a $CRONFILE
}

get_arch
updating
install_basics
install_requirements
install_mysql
setup_mysql
install_grafana
create_cron
start_grafana

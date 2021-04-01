#!/bin/bash

RASP_MOD_A="Raspberry Pi Model A"
RASP_MOD_B="Raspberry Pi 3 Model B"
MODEL_FILE="/sys/firmware/devicetree/base/model"
IS_TYPE_A=false
IS_TYPE_B=false
ERROR_MOD_NOT_FOUND="Undetected Raspberry Pi Model"
CRONJOB="@reboot python3 /home/pi/habitatController/main.py"
CRONFILE="/var/spool/cron/crontabs/pi"
CRONCAT="sudo cat $CRONFILE"
TMPFILE="/tmp/tmpCronJobs.txt"
GRAFANA_ENABLE="sudo /bin/systemctl enable grafana-server"
GRAFANA_START="sudo /bin/systemctl start grafana-server"
GRAFANA_ENABLED="Loaded: loaded (/lib/systemd/system/grafana-server.service; enabled"
GRAFANA_RUNNING="Active: active (running)"
IS_GRAFANA_ENABLED=false
IS_GRAFANA_RUNNING=false

get_arch() {
  echo "Detecting Raspberry Pi type"
  if grep -q "$RASP_MOD_A" "$MODEL_FILE"; then
    echo "$RASP_MOD_A detected"
    IS_TYPE_A=true
  elif grep -q "$RASP_MOD_B" "$MODEL_FILE"; then
    echo "$RASP_MOD_B detected"
    IS_TYPE_B=true
  else
    echo "Undetected Raspberry Pi Model"
  fi
}

uninstall_mysql() {
  echo "Installing items for mySql"
  sudo apt-get remove -y mariadb-server python-mysqldb
}

uninstall_grafana() {
  sudo apt-get remove -y grafana
}

uninstall_cleanup() {
  sudo apt autoremove -y
}

get_arch
uninstall_mysql
uninstall_grafana
uninstall_cleanup

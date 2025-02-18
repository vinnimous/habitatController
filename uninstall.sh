#!/bin/bash

# Define colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

RASP_MOD_A="Raspberry Pi Model A"
RASP_MOD_B="Raspberry Pi 3 Model B"
MODEL_FILE="/sys/firmware/devicetree/base/model"
IS_TYPE_A=false
IS_TYPE_B=false
ERROR_MOD_NOT_FOUND="Undetected Raspberry Pi Model"
CRONJOB="@reboot /home/pi/habitatController/venv/bin/python3 /home/pi/habitatController/main.py"
CRONFILE="/var/spool/cron/crontabs/pi"
CRONCAT="sudo cat $CRONFILE"
TMPFILE="/tmp/tmpCronJobs.txt"
GRAFANA_ENABLE="sudo /bin/systemctl enable grafana-server"
GRAFANA_START="sudo /bin/systemctl start grafana-server"
GRAFANA_ENABLED="Loaded: loaded (/lib/systemd/system/grafana-server.service; enabled"
GRAFANA_RUNNING="Active: active (running)"
IS_GRAFANA_ENABLED=false
IS_GRAFANA_RUNNING=false

# Determine Raspberry Pi architecture
get_arch() {
  echo -e "${GREEN}Detecting Raspberry Pi type${NC}"
  if grep -q "$RASP_MOD_A" "$MODEL_FILE"; then
    echo -e "${GREEN}$RASP_MOD_A detected${NC}"
    IS_TYPE_A=true
  elif grep -q "$RASP_MOD_B" "$MODEL_FILE"; then
    echo -e "${GREEN}$RASP_MOD_B detected${NC}"
    IS_TYPE_B=true
  else
    echo -e "${RED}Undetected Raspberry Pi Model${NC}"
  fi
}

# Uninstall MySQL and related packages
uninstall_mysql() {
  echo -e "${GREEN}Uninstalling MySQL${NC}"
  sudo apt-get remove -y mariadb-server python3-mysqldb
}

# Uninstall Grafana
uninstall_grafana() {
  echo -e "${GREEN}Uninstalling Grafana${NC}"
  sudo apt-get remove -y grafana
  sudo rm -f /etc/apt/sources.list.d/grafana.list
  sudo userdel -r grafanauser
}

# Remove Python virtual environment and related packages
uninstall_python_env() {
  echo -e "${GREEN}Removing Python virtual environment${NC}"
  rm -rf /home/pi/habitatController/venv
}

# Remove cron job
remove_cron() {
  echo -e "${GREEN}Removing cron job${NC}"
  crontab -l | grep -v "$CRONJOB" | crontab -
}

# Clean up system
uninstall_cleanup() {
  echo -e "${GREEN}Cleaning up system${NC}"
  sudo apt autoremove -y
}

# Execute the functions in order
get_arch
uninstall_mysql
uninstall_grafana
uninstall_python_env
remove_cron
uninstall_cleanup

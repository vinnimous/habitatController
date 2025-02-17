#!/bin/bash

RASP_MOD_A="Raspberry Pi Model A"
RASP_MOD_B="Raspberry Pi 3 Model B"
MODEL_FILE="/sys/firmware/devicetree/base/model"
IS_TYPE_A=false
IS_TYPE_B=false
ERROR_MOD_NOT_FOUND="Undetected Raspberry Pi Model"
CRONJOB="@reboot /home/pi/habitatController/venv/bin/python3 /home/pi/habitatController/main.py"
CRONFILE="/var/spool/cron/crontabs/pi"
CRONCAT="sudo cat $CRONFILE"
TMPFILE="/etc/cron.d/schedule"
GRAFANA_ENABLE="sudo /bin/systemctl enable grafana-server"
GRAFANA_START="sudo /bin/systemctl start grafana-server"
GRAFANA_RUNNING="active"
IS_GRAFANA_RUNNING=false

#Determine Raspberry Pi architecture to select correct packages
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

#Updating
updating() {
  echo "Updating libraries"
  sudo apt-get update -y
}

#Installing basic requirements
install_basics() {
  echo "Installing some basic build tools"
  sudo apt-get install -y build-essential python3-dev python3-smbus python3-pip python3-venv
}

#Installing Python specific requirements
install_requirements() {
  echo "Setting up Python virtual environment"
  python3 -m venv venv  # Create a virtual environment named 'venv'
  source venv/bin/activate  # Activate the virtual environment
  echo "Installing requirements in the virtual environment"
  pip install -r requirements.txt  # Install packages in the virtual environment
  deactivate  # Deactivate the virtual environment
}

#Installing MySQL
install_mysql() {
  echo "Installing items for mySql"
  sudo apt-get install -y apt-transport-https software-properties-common wget mariadb-server adduser libfontconfig1
  sudo apt-get install -y python3-mysqldb expect
}

#Selecing which Grafana package to install based on Raspberry Pi architecture
install_grafana() {
  echo "Installing Grafana"
  if $IS_TYPE_B; then
    grafana_apt
  elif $IS_TYPE_A; then
    grafana_deb
  else
    echo "$ERROR_MOD_NOT_FOUND"
  fi
}

#Grafana installation for arm
grafana_deb() {
  wget https://dl.grafana.com/oss/release/grafana-rpi_7.3.4_armhf.deb
  sudo dpkg -i grafana-rpi_7.3.4_armhf.deb
}

#Grafana installation for apt
grafana_apt() {
  wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
  echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
  sudo apt-get update
  sudo apt-get install -y grafana
}

#Starting Grafana
start_grafana() {
  echo "Starting Grafana"
  if $IS_TYPE_B; then
    sudo /bin/systemctl enable grafana-server
    sudo /bin/systemctl start grafana-server &
  elif $IS_TYPE_A; then
    sudo service grafana-server start &
    sudo update-rc.d grafana-server defaults
  else
    echo "$ERROR_MOD_NOT_FOUND"
  fi
}

#Checking to see if Grafana is properly running
check_grafana() {
  if systemctl is-active grafana-server | grep -q "$GRAFANA_RUNNING"; then
    echo "Grafana is currently running"
    IS_GRAFANA_RUNNING=true
  else
    echo "Grafana may have failed, please confirm manually"
  fi
}

#Requires minor interaction and to complete
setup_mysql() {
  echo "Setting up mySql"
  expect <<EOF
spawn sudo mysql_secure_installation

# Expect prompts and send responses to avoid interaction
expect "Enter current password for root (enter for none):"
send "\r"  # No password for the current root user

expect "Set root password?"
send "N\r"  # No, root password left empty

expect "Remove anonymous users?"
send "Y\r"  # Yes, remove anonymous users

expect "Disallow root login remotely?"
send "N\r"  # No, allow root login remotely

expect "Remove test database and access to it?"
send "Y\r"  # Yes, remove the test database

expect "Reload privilege tables now?"
send "Y\r"  # Yes, reload the privilege tables

expect eof
EOF
  sudo mysql -u root -p <createDB.sql
}

#Trying to create a cronjob
create_cron() {
  echo "Trying to create a cronjob"
  (
    crontab -l
    echo "$CRONJOB"
  ) | awk '!x[$0]++' | crontab -
  if crontab -l | grep -q "$CRONJOB"; then
    echo "Successfully created cronjob"
  else
    echo "Cronjob creation failed, attempting schedule"
    create_schedule
  fi
}

#If the previous cronjob creation fails it will attempt to create it as a schedule
create_schedule() {
  sudo touch /etc/cron.d/schedule
  sudo echo "$CRONJOB" >$TMPFILE
  sudo chmod 600 $TMPFILE
}

configure_grafana() {
  bash grafana_setup.sh
}

restart() {
  echo "Removing left overs and restarting"
  sudo apt autoremove -y
  sudo shutdown -r
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
check_grafana
configure_grafana
restart

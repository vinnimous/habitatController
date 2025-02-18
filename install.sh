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
TMPFILE="/etc/cron.d/schedule"
GRAFANA_ENABLE="sudo /bin/systemctl enable grafana-server"
GRAFANA_START="sudo /bin/systemctl start grafana-server"
GRAFANA_RUNNING="active"
IS_GRAFANA_RUNNING=false

# Determine Raspberry Pi architecture to select correct packages
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

# Update package lists
updating() {
  echo -e "${GREEN}Updating libraries${NC}"
  sudo apt-get update -y
}

# Install basic build tools and Python dependencies
install_basics() {
  echo -e "${GREEN}Installing some basic build tools${NC}"
  sudo apt-get install -y build-essential python3-dev python3-smbus python3-pip python3-venv
}

# Set up Python virtual environment and install requirements
install_requirements() {
  echo -e "${GREEN}Setting up Python virtual environment${NC}"
  python3 -m venv venv  # Create a virtual environment named 'venv'
  source venv/bin/activate  # Activate the virtual environment
  echo -e "${GREEN}Installing requirements in the virtual environment${NC}"
  pip install -r requirements.txt  # Install packages in the virtual environment
  deactivate  # Deactivate the virtual environment
}

# Install MySQL and related packages
install_mysql() {
  echo -e "${GREEN}Installing items for MySQL${NC}"
  sudo apt-get install -y apt-transport-https software-properties-common wget mariadb-server adduser libfontconfig1
  sudo apt-get install -y python3-mysqldb expect
}

# Select which Grafana package to install based on Raspberry Pi architecture
install_grafana() {
  echo -e "${GREEN}Installing Grafana${NC}"
  if $IS_TYPE_B; then
    grafana_apt
  elif $IS_TYPE_A; then
    grafana_deb
  else
    echo -e "${RED}$ERROR_MOD_NOT_FOUND${NC}"
  fi
}

# Grafana installation for arm architecture
grafana_deb() {
  wget https://dl.grafana.com/oss/release/grafana-rpi_7.3.4_armhf.deb
  sudo dpkg -i grafana-rpi_7.3.4_armhf.deb
}

# Grafana installation using apt
grafana_apt() {
  wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
  echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
  sudo apt-get update -y
  sudo apt-get install -y grafana
}

# Start Grafana service
start_grafana() {
  echo -e "${GREEN}Starting Grafana${NC}"
  if $IS_TYPE_B; then
    sudo /bin/systemctl enable grafana-server
    sudo /bin/systemctl start grafana-server &
  elif $IS_TYPE_A; then
    sudo service grafana-server start &
    sudo update-rc.d grafana-server defaults
  else
    echo -e "${RED}$ERROR_MOD_NOT_FOUND${NC}"
  fi
}

# Check if Grafana is running
check_grafana() {
  if systemctl is-active grafana-server | grep -q "$GRAFANA_RUNNING"; then
    echo -e "${GREEN}Grafana is currently running${NC}"
    IS_GRAFANA_RUNNING=true
  else
    echo -e "${RED}Grafana may have failed, please confirm manually${NC}"
  fi
}

# Set up MySQL with secure installation
setup_mysql() {
  echo -e "${GREEN}Setting up MySQL${NC}"
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

# Create a cron job to run the main script at reboot
create_cron() {
  echo -e "${GREEN}Trying to create a cronjob${NC}"
  (
    crontab -l
    echo "$CRONJOB"
  ) | awk '!x[$0]++' | crontab -
  if crontab -l | grep -q "$CRONJOB"; then
    echo -e "${GREEN}Successfully created cronjob${NC}"
  else
    echo -e "${RED}Cronjob creation failed, attempting schedule${NC}"
    create_schedule
  fi
}

# If cron job creation fails, create a schedule
create_schedule() {
  sudo touch /etc/cron.d/schedule
  sudo echo "$CRONJOB" >$TMPFILE
  sudo chmod 600 $TMPFILE
}

# Configure Grafana
configure_grafana() {
  bash grafana_setup.sh
}

# Clean up and restart the system
restart() {
  echo -e "${GREEN}Removing leftovers and restarting${NC}"
  sudo apt autoremove -y
  sudo shutdown -r
}

# Execute the functions in order
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

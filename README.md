# habitatController
This is my project to build a simple raspberry pi controlled habitat with inexpensive parts that anyone can build. Parts
used are relays and temp sensor.

## Prerequisites

    sudo apt-get install -y build-essential python-dev python-smbus python3-pip python-mysqldb

## Enable the following

    sudo raspi-config

- gpio
- i2c
- spi

enable gpio, i2c, spi

## This will also install Grafana and SQLLite3

### Grafana Package details

- Installs binary to /usr/sbin/grafana-server
- Installs Init.d script to /etc/init.d/grafana-server
- Creates default file (environment vars) to /etc/default/grafana-server
- Installs configuration file to /etc/grafana/grafana.ini
- Installs systemd service (if systemd is available) name grafana-server.service
- The default configuration sets the log file at /var/log/grafana/grafana.log
- The default configuration specifies a SQLite3 db at /var/lib/grafana/grafana.db
- Installs HTML/JS/CSS and other Grafana files at /usr/share/grafana

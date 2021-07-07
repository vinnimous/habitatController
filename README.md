# habitatController

I wasn't happy with the expensive habitat controllers. I wanted to be able to use the same type of device on nearly
anything that requires climate controls including plants as well as animals.

So what makes this one special?

- Calculated solar cycles and seasons based on desired locations
- Nocturnal heat control
- Completely contained historical data and reporting through MYSQL and Grafana
- Very easy to build and easily replaceable parts

## Parts list

- Raspberry Pi (3 or greater is recommended however it should work with a Zero)
- Relays
- Temperature sensor (mpc9808)
- Your choice of lights and heaters

## Prerequisites

All prerequisites and needed packages will be installed.

### Relay connections

- Standard light = 17
- UVB light = 22
- Night light = 23
- Heater = 27

## Enable the following

    sudo raspi-config

- gpio
- i2c
- spi

## Grafana

- Grafana will install SQLLite3 by default.
- MySQL will be used as a datasource by the habitat controller which removes records older than 30 days.
- Default dashboards will be created for current and historical views

## What's next?

In the future I plan to update to include wind activity and temperature variations to simulate weather. Beyond that the
goal is to include activity, water, and food monitoring.
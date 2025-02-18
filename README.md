# habitatController

I wasn't happy with the expensive habitat controllers. I wanted to be able to use the same type of device on nearly
anything that requires climate controls including plants as well as animals.

So what makes this one special?

- Calculated solar cycles and seasons based on desired locations
- Nocturnal heat control
- Completely contained historical data and reporting through MYSQL and Grafana
- Very easy to build and easily replaceable parts

Temperature range information based on [Caring for your Bearded Dragon](https://cvm.ncsu.edu/wp-content/uploads/2016/12/Caring-for-your-Bearded-Dragon.pdf#:~:text=Temperature%3A%20Daytime%20maintain%20between%2075,hot%20ends%20of%20the%20enclosure).

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

## Wiring Diagram

Here is the wiring diagram for the habitat controller:

![Wiring Diagram](wiring_diagram.png)

- **Pin 17**: Standard light
- **Pin 22**: UVB light
- **Pin 23**: Night light
- **Pin 27**: Heater
- **Temperature sensor (mpc9808)**: Connected to I2C pins (SDA, SCL)

## Grafana

- Grafana will install SQLLite3 by default.
- MySQL will be used as a datasource by the habitat controller which removes records older than 30 days.
- Default dashboards will be created for current and historical views

## What's next?

In the future I plan to update to include wind activity and temperature variations to simulate weather. Beyond that the
goal is to include activity, water, and food monitoring.
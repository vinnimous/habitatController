import logging

try:
    import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
except (ImportError, RuntimeError):
    from mock_gpio import GPIO  # Import mock GPIO library

logger = logging.getLogger('relay')

pin_light = 17
pin_heater = 27
pin_uvb = 22
pin_night = 23
pin_bubbler = 24

relayLog = "\"Relays: {} UVB: {} Heat: {} Night: {} Bubbler: {}\"" \
           ".format(GPIO.input(pin_light), (GPIO.input(pin_uvb)), GPIO.input(pin_heater), GPIO.input(pin_night), GPIO.input(pin_bubbler))"(pin_light, pin_uvb, pin_heater, pin_night, pin_bubbler)


def setup():
    GPIO.setwarnings(False)  # Ignore warning for now
    GPIO.setmode(GPIO.BCM)  # Use BCM numbering
    GPIO.setup(pin_light, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(pin_uvb, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(pin_heater, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(pin_night, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(pin_bubbler, GPIO.OUT, initial=GPIO.HIGH)
    logger.debug(relayLog)


def day_light():
    GPIO.output(pin_light, GPIO.LOW)  # Turn on light bulb
    GPIO.output(pin_uvb, GPIO.LOW)  # Turn on UVB light
    GPIO.output(pin_night, GPIO.HIGH)  # Turn off night light
    logger.debug(relayLog)


def night_light():
    GPIO.output(pin_light, GPIO.HIGH)  # Turn off light bulb
    GPIO.output(pin_uvb, GPIO.HIGH)  # Turn off UVB light
    GPIO.output(pin_night, GPIO.LOW)  # Turn on night light
    logger.debug(relayLog)


def emergency_heat():
    GPIO.output(pin_light, GPIO.LOW)  # Turn on light bulb
    GPIO.output(pin_uvb, GPIO.LOW)  # Turn on UVB light
    GPIO.output(pin_heater, GPIO.LOW)  # Turn on heat
    GPIO.output(pin_night, GPIO.LOW)  # Turn on night light
    logger.debug(relayLog)


def all_off():
    GPIO.output(pin_light, GPIO.HIGH)  # Turn off light bulb
    GPIO.output(pin_uvb, GPIO.HIGH)  # Turn off UVB light
    GPIO.output(pin_heater, GPIO.HIGH)  # Turn off heat
    GPIO.output(pin_night, GPIO.HIGH)  # Turn off night light
    logger.debug(relayLog)


def heater_on():
    GPIO.output(pin_heater, GPIO.LOW)  # Turn on heater bulb
    logger.debug(relayLog)


def heater_off():
    GPIO.output(pin_heater, GPIO.HIGH)  # Turn off heater bulb
    logger.debug(relayLog)


def bubbler_on():
    GPIO.output(pin_bubbler, GPIO.LOW)  # Turn on bubbler
    logger.debug(relayLog)

def bubbler_off():
    GPIO.output(pin_bubbler, GPIO.HIGH)  # Turn off bubbler
    logger.debug(relayLog)

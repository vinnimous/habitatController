import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library

pin_light = 17
pin_heater = 27
pin_uvb = 22
pin_night = 23


def setup():
    GPIO.setwarnings(False)  # Ignore warning for now
    GPIO.setmode(GPIO.BCM)  # Use BCM numbering
    GPIO.setup(pin_light, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(pin_uvb, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(pin_heater, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(pin_night, GPIO.OUT, initial=GPIO.HIGH)
    

def day_light():
    GPIO.output(pin_light, GPIO.LOW)  # Turn on light bulb
    GPIO.output(pin_uvb, GPIO.LOW)  # Turn on UVB light
    GPIO.output(pin_night, GPIO.HIGH)  # Turn off night light


def night_light():
    GPIO.output(pin_light, GPIO.HIGH)  # Turn off light bulb
    GPIO.output(pin_uvb, GPIO.HIGH)  # Turn off UVB light
    GPIO.output(pin_night, GPIO.LOW)  # Turn on night light

    
def day_light():
    GPIO.output(pin_light, GPIO.LOW)  # Turn on light bulb
    GPIO.output(pin_uvb, GPIO.LOW)  # Turn on UVB light
    GPIO.output(pin_night, GPIO.HIGH)  # Turn off night light
    
    
def night_light():
    GPIO.output(pin_light, GPIO.HIGH)  # Turn off light bulb
    GPIO.output(pin_uvb, GPIO.HIGH)  # Turn off UVB light
    GPIO.output(pin_night, GPIO.LOW)  # Turn on night light


def emergency_heat():
    GPIO.output(pin_light, GPIO.LOW)  # Turn on light bulb
    GPIO.output(pin_uvb, GPIO.LOW)  # Turn on UVB light
    GPIO.output(pin_heater, GPIO.LOW)  # Turn on heat
    GPIO.output(pin_night, GPIO.LOW)  # Turn on night light

    
def all_off():
    GPIO.output(pin_light, GPIO.HIGH)  # Turn off light bulb
    GPIO.output(pin_uvb, GPIO.HIGH)  # Turn off UVB light
    GPIO.output(pin_heater, GPIO.HIGH)  # Turn off heat
    GPIO.output(pin_night, GPIO.HIGH)  # Turn off night light


def heater_on():
    GPIO.output(pin_heater, GPIO.LOW)  # Turn on heater bulb


def heater_off():
    GPIO.output(pin_heater, GPIO.HIGH)  # Turn off heater bulb

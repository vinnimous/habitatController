import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library


pin_light = 11
pin_heater = 13
pin_uvb = 15
pin_night = 16



def setup():
    GPIO.setwarnings(False)    # Ignore warning for now
    GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering
    GPIO.setup(pin_light, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(pin_uvb, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(pin_heater, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(pin_night, GPIO.OUT, initial=GPIO.LOW)

def day_light():
    GPIO.output(pin_light, GPIO.HIGH) # Turn on light bulb
    GPIO.output(pin_uvb, GPIO.HIGH) # Turn on UVB light
    GPIO.output(pin_night, GPIO.LOW)  # Turn off night light
def night_light():
    GPIO.output(pin_light, GPIO.LOW)  # Turn off light bulb
    GPIO.output(pin_uvb, GPIO.LOW)  # Turn off UVB light
    GPIO.output(pin_night, GPIO.HIGH) # Turn on night light
def emergency_heat():
    GPIO.output(pin_light, GPIO.HIGH)  # Turn on light bulb
    GPIO.output(pin_uvb, GPIO.HIGH)  # Turn on UVB light
    GPIO.output(pin_heater, GPIO.HIGH)  # Turn on heat
    GPIO.output(pin_night, GPIO.HIGH)  # Turn on night light
def all_off():
    GPIO.output(pin_light, GPIO.LOW)  # Turn off light bulb
    GPIO.output(pin_uvb, GPIO.LOW)  # Turn off UVB light
    GPIO.output(pin_heater, GPIO.LOW)  # Turn off heat
    GPIO.output(pin_night, GPIO.LOW)  # Turn off night light

def heater_on():
    GPIO.output(pin_heater, GPIO.HIGH)

def heater_off():
    GPIO.output(pin_heater, GPIO.LOW)
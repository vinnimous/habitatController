import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library

DAYLIGHT = 11
DAYUVB = 13
HEAT = 15
NIGHTLIGHT = 15

def setup():
    GPIO.setwarnings(False)    # Ignore warning for now
    GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering
    GPIO.setup(DAYLIGHT, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(DAYUVB, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(16, GPIO.OUT, initial=GPIO.LOW)

def dayLight():
    GPIO.output(DAYLIGHT, GPIO.HIGH) # Turn on light bulb
    GPIO.output(DAYUVB, GPIO.HIGH) # Turn on UVB light
    GPIO.output(NIGHTLIGHT, GPIO.LOW)  # Turn off night light
def nightLight():
    GPIO.output(DAYLIGHT, GPIO.LOW)  # Turn off light bulb
    GPIO.output(DAYUVB, GPIO.LOW)  # Turn off UVB light
    GPIO.output(NIGHTLIGHT, GPIO.HIGH) # Turn on night light
def emergencyHeat():
    GPIO.output(DAYLIGHT, GPIO.HIGH)  # Turn on light bulb
    GPIO.output(DAYUVB, GPIO.HIGH)  # Turn on UVB light
    GPIO.output(HEAT, GPIO.HIGH)  # Turn on heat
    GPIO.output(NIGHTLIGHT, GPIO.HIGH)  # Turn on night light
def allOff():
    GPIO.output(DAYLIGHT, GPIO.LOW)  # Turn off light bulb
    GPIO.output(DAYUVB, GPIO.LOW)  # Turn off UVB light
    GPIO.output(HEAT, GPIO.LOW)  # Turn off heat
    GPIO.output(NIGHTLIGHT, GPIO.LOW)  # Turn off night light

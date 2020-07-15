import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library


dayLight = 17
heater = 27
dayUVB = 22
nightLight = 23



def setup():
    GPIO.setwarnings(False)    # Ignore warning for now
    GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering
    GPIO.setup(dayLight, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(dayUVB, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(heater, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(nightLight, GPIO.OUT, initial=GPIO.LOW)

def dayLight():
    GPIO.output(dayLight, GPIO.HIGH) # Turn on light bulb
    GPIO.output(dayUVB, GPIO.HIGH) # Turn on UVB light
    GPIO.output(nightLight, GPIO.LOW)  # Turn off night light
def nightLight():
    GPIO.output(dayLight, GPIO.LOW)  # Turn off light bulb
    GPIO.output(dayUVB, GPIO.LOW)  # Turn off UVB light
    GPIO.output(nightLight, GPIO.HIGH) # Turn on night light
def emergencyHeat():
    GPIO.output(dayLight, GPIO.HIGH)  # Turn on light bulb
    GPIO.output(dayUVB, GPIO.HIGH)  # Turn on UVB light
    GPIO.output(heater, GPIO.HIGH)  # Turn on heat
    GPIO.output(nightLight, GPIO.HIGH)  # Turn on night light
def allOff():
    GPIO.output(dayLight, GPIO.LOW)  # Turn off light bulb
    GPIO.output(dayUVB, GPIO.LOW)  # Turn off UVB light
    GPIO.output(heater, GPIO.LOW)  # Turn off heat
    GPIO.output(nightLight, GPIO.LOW)  # Turn off night light

def heater_on():
    GPIO.output(heater, GPIO.HIGH)

def heater_off():
    GPIO.output(heater, GPIO.LOW)
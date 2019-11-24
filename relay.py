#!/usr/bin/python

import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
from time import sleep     # Import the sleep function from the time module

GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering
GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(13, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(16, GPIO.OUT, initial=GPIO.LOW)

def dayLight():
    GPIO.output(11, GPIO.HIGH) # Turn on light bulb
    GPIO.output(13, GPIO.HIGH) # Turn on UVB light
    GPIO.output(16, GPIO.LOW)  # Turn off night light
def nightLight():
    GPIO.output(11, GPIO.LOW)  # Turn off light bulb
    GPIO.output(13, GPIO.LOW)  # Turn off UVB light
    GPIO.output(16, GPIO.HIGH) # Turn on night light


while True: # Run forever
    dayLight()  #test
    sleep(1)                  # Sleep for 1 second
    nightLight()
    sleep(1)                  # Sleep for 1 second

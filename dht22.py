import Adafruit_DHT
import time as sleep

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

while True:
    h, t = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    # Confirm valid temp and humidity
    if isinstance(h, float) and isinstance(t, float):
        t = t * 9 / 5.0 + 32  # Convert to Fahrenheit
        print('    Temp: {0:0.1f}'.format(t))
        print(223, True)  # Display degree symbol
        print('F\nHumidity: {0:0.1f}%'.format(h))
    else:
        print('Error...')
    sleep(4)
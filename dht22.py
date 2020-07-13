import Adafruit_DHT
import time
import errorMessages

hotSensor = Adafruit_DHT.DHT22
hotPin = 4

coldSensor = Adafruit_DHT.DHT22
coldPin = 6

while True:
    h_hot, tHot = Adafruit_DHT.read_retry(hotSensor, hotPin)
    t_hot = tHot * 9 / 5.0 + 32  # Convert to Fahrenheit
    h_cold, tCold = Adafruit_DHT.read_retry(coldSensor, coldPin)
    t_cold = tCold * 9 / 5.0 + 32  # Convert to Fahrenheit
    if h_hot is not None and t_hot is not None:
        print("Temp={0:0.1f}*F  Humidity={1:0.1f}%".format(t_hot, h_hot))
    else:
        print(errorMessages.E5)
    if h_cold is not None and t_cold is not None:
        print("Temp={0:0.1f}*F  Humidity={1:0.1f}%".format(t_cold, h_cold))
    else:
        print(errorMessages.E6)
    time.sleep(4)
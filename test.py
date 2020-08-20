import adafruit_mcp9808
import busio
from adafruit_blinka import board

with busio.I2C(board.SCL,board.SDA) as i2c:
    t = adafruit_mcp9808.MCP9808(i2c)

    # Finally, read the temperature property and print it out
    print(t.temperature)
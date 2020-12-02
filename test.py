import time
import board
import busio
import adafruit_mcp9808

# i2c_bus = busio.I2C(board.SCL, board.SDA)

# To initialize  e using the default address:
# mcp = adafruit_mcp9808.MCP9808(i2c_bus)

# To initialize using a specified address:
# Necessary when, for example, connecting A0 to VDD to make address=0x19
# mcp = adafruit_mcp9808.MCP9808(i2c_bus, address=0x19)


while True:
    tempF = adafruit_mcp9808.MCP9808(busio.I2C(board.SCL, board.SDA)).temperature * 9 / 5 + 32
    print("Temperature: {} F ".format(tempF))
    time.sleep(2)

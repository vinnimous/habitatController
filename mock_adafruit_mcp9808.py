class MockMCP9808:
    def __init__(self, i2c, address=0x18):
        self._temperature = 25.0  # Default mock temperature in Celsius

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        self._temperature = value

MCP9808 = MockMCP9808

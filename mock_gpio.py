class MockGPIO:
    BCM = "BCM"
    OUT = "OUT"
    HIGH = "HIGH"
    LOW = "LOW"

    def setwarnings(self, flag):
        pass

    def setmode(self, mode):
        pass

    def setup(self, pin, mode, initial=None):
        pass

    def output(self, pin, state):
        pass

    def input(self, pin):
        return self.HIGH

    def cleanup(self):
        pass

GPIO = MockGPIO()

import RPi.GPIO as GPIO
import time


class ShiftInput:
    highFlag = False
    receivedData = ''

    def __init__(self):

        # GPIO Setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.OCTAVEUP = 6
        self.OCTAVEDOWN = 12

        self.SERIALNCM = 13  # Input for NCM(s)
        self.CLOCK = 9  #
        self.PLOAD = 11  # Equivalent to LATCH?

        # old = ''
        GPIO.setup(self.SERIALNCM, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.OCTAVEUP, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.OCTAVEDOWN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.setup(self.PLOAD, GPIO.OUT)
        GPIO.setup(self.CLOCK, GPIO.OUT)

        GPIO.output(self.PLOAD, 1)

        GPIO.output(self.CLOCK, 0)

    # Pulses the latch pin - write the output to data lines
    def loadData(self):
        GPIO.output(self.PLOAD, 0)

        time.sleep(0.0001)

        GPIO.output(self.PLOAD, 1)

    # Pulses clock to shift bits
    def tick(self):
        GPIO.output(self.CLOCK, 0)

        GPIO.output(self.CLOCK, 1)

        time.sleep(0.0001)

        GPIO.output(self.CLOCK, 0)

    def readData(self):
        receivedByte = ''
        highFlag = False

        self.loadData()
        idx = 0

        for x in range(40):
            idx += 1
            i = GPIO.input(self.SERIALNCM)
            if i:
                highFlag = True
                receivedByte += str(idx) + ", "

            self.tick()

        return [highFlag, receivedByte]


shiftInput = ShiftInput()
print("Starting")

while True:
    # Get input, print IDs if any input is high
    if shiftInput.readData()[0]:
        print(shiftInput.readData()[1])
        time.sleep(2)

    time.sleep(0.05)

import RPi.GPIO as GPIO
import time

class ShiftInput:

  def __init__(self):

    # GPIO Setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    self.OCTAVEUP = 6
    self.OCTAVEDOWN = 12

    self.SERIALNCM = 13        # Input for NCM(s)
    self.SERIALGCM = 5         # Input for General Control Module
    self.CLOCK = 19            # 
    self.PLOAD = 26            # Equivalent to LATCH?

    #old = ''
    GPIO.setup(self.SERIALNCM, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(self.SERIALGCM, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(self.OCTAVEUP, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(self.OCTAVEDOWN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    GPIO.setup(self.PLOAD, GPIO.OUT)
    #GPIO.setup(self.CLOCKENABLE, GPIO.OUT)
    GPIO.setup(self.CLOCK, GPIO.OUT)

    GPIO.output(self.PLOAD, 1)
    #GPIO.output(self.CLOCKENABLE, 1)
    GPIO.output(self.CLOCK, 0)

  # Pulses the latch pin - write the output to data lines
  def loadData(self):
    GPIO.output(self.PLOAD, 0)
    time.sleep(0.0001)
    GPIO.output(self.PLOAD, 1)
    #time.sleep(0.1)

  # Pulses clock to shift bits
  def tick(self):
    GPIO.output(self.CLOCK, 0)
    #time.sleep(0.005)
    GPIO.output(self.CLOCK, 1)
    time.sleep(0.0001)
    GPIO.output(self.CLOCK, 0)
    #time.sleep(1)

  def readData(self):
    # Gets data from shift register and seperate pins (couldn't hook everything up in one go yet)

    receivedByte = ''
    receivedGCMByte = ''

    self.loadData()
    
    #GPIO.output(self.CLOCKENABLE, 0)

    ocUp = GPIO.input(self.OCTAVEUP)
    ocDown = GPIO.input(self.OCTAVEDOWN)

    for x in range(8):
      i = GPIO.input(self.SERIALNCM)
      o = GPIO.input(self.SERIALGCM)

      receivedByte += str(i)
      receivedGCMByte += str(o)
      self.tick()

    #GPIO.output(self.CLOCKENABLE, 1)

    output = str(ocUp) + str(ocDown) + receivedByte + receivedGCMByte

    return output
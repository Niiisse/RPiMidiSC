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
    self.CLOCK = 9            # 
    self.PLOAD = 11            # Equivalent to LATCH?

    #old = ''
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

    GPIO.output(self.CLOCK, ft0)

  def readData(self):
    """ Reads data from input shift registers
    
    Two seperate for loops: 8 ticks for NCM (8 ticks * NCM count)
    16 ticks for input of GCM """

    receivedByte = ''

    self.loadData()
    
    #GPIO.output(self.CLOCKENABLE, 0)

    ocUp = GPIO.input(self.OCTAVEUP)
    ocDown = GPIO.input(self.OCTAVEDOWN)

    for x in range(40):
        i = GPIO.input(self.SERIALNCM)
        receivedByte += str(i)

        self.tick()

    #for x in range(16):
    #  o = GPIO.input(self.SERIALGCM)
    #  receivedGCMByte += str(o)
      
    #  self.tick()


    output = str(ocUp) + str(ocDown) + receivedByte 
    return output

shiftInput = ShiftInput()

while True:
  print(shiftInput.readData())
  time.sleep(0.05)

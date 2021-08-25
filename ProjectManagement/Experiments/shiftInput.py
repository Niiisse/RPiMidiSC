import RPi.GPIO as GPIO
import time

class NoteModule:
  def __init__(self):

    # GPIO Setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    self.OCTAVEUP = 6
    self.OCTAVEDOWN = 12

    self.SERIAL = 13
    self.CLOCK = 19
    #self.CLOCKENABLE = 6
    self.PLOAD = 26

    #old = ''

    GPIO.setup(self.SERIAL, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
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
    time.sleep(0.001)
    GPIO.output(self.PLOAD, 1)
    #time.sleep(0.1)

  # Pulses clock to shift bits
  def tick(self):
    GPIO.output(self.CLOCK, 0)
    #time.sleep(0.005)
    GPIO.output(self.CLOCK, 1)
    time.sleep(0.002)
    GPIO.output(self.CLOCK, 0)
    #time.sleep(1)

  def readData(self):
    # TODO: get additional two inputs 

    receivedByte = ''
    self.loadData()
    
    #tick()
    #GPIO.output(self.CLOCKENABLE, 0)

    ocUp = GPIO.input(self.OCTAVEUP)
    ocDown = GPIO.input(self.OCTAVEDOWN)
    print(ocUp, end=', ')
    print(ocDown, end=', ')

    for x in range(8):
      i = GPIO.input(self.SERIAL)
      print(i, end=', ')
      receivedByte += str(i)
      self.tick()

    print("")

    #GPIO.output(self.CLOCKENABLE, 1)

    #time.sleep(0.2)
    return receivedByte

noteModule = NoteModule()

while True:
  noteModule.readData()
import RPi.GPIO as GPIO
import math
import time

class ShiftRegister:

  def __init__(self, data, latch, clock):
    self.DATA = data
    self.LATCH = latch
    self.CLOCK = clock

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(self.DATA,  GPIO.OUT)
    GPIO.setup(self.LATCH, GPIO.OUT)
    GPIO.setup(self.CLOCK, GPIO.OUT)

  # Pulses the latch pin - write the output to data lines
  def latch(self):
    GPIO.output(self.LATCH, 0)
    GPIO.output(self.LATCH, 1)
    GPIO.output(self.LATCH, 0)
    #print("Latched")

  # Pulses clock to shift bits
  def tick(self):
    GPIO.output(self.CLOCK, 0)
    GPIO.output(self.CLOCK, 1)
    GPIO.output(self.CLOCK, 0)

  # Clears all outputs by writing an empty byte
  def clear(self):
    GPIO.output(self.DATA, 0)

    for x in range(0, 8):
      GPIO.output(self.CLOCK, 0)
      GPIO.output(self.CLOCK, 1)  
      GPIO.output(self.CLOCK, 0)  

    self.latch()

  # Push bit into the shift register
  def inputBit(self, inputValue):
    GPIO.output(self.DATA, inputValue)
    self.tick()

  # Push a byte to the shift register
  # Takes a string, by the way:
  #   bytestring = format(numericArr[0], '08b')
  #   outputBits(bytestring)
  #  Then, splits input values into individual values
  
  def outputBits(self, inputString):
    bitList = list(inputString)
    bitList = bitList[::-1]

    for bit in bitList:
      bit = int(bit)
      
      self.inputBit(bit)
    
    self.latch()
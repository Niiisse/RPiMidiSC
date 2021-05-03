import RPi.GPIO as GPIO
import time

class ShiftRegister():
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)

  DATA  = 21
  LATCH = 20
  CLOCK = 16

  GPIO.setup(DATA,  GPIO.OUT)
  GPIO.setup(LATCH, GPIO.OUT)
  GPIO.setup(CLOCK, GPIO.OUT)

  # Pulses the latch pin - write the output to data lines
  def latch():
    GPIO.output(LATCH, 0)
    GPIO.output(LATCH, 1)
    GPIO.output(LATCH, 0)
    #print("Latched")

  # Pulses clock to shift bits
  def tick():
    GPIO.output(CLOCK, 0)
    GPIO.output(CLOCK, 1)
    GPIO.output(CLOCK, 0)

  # Clears all outputs by writing an empty byte
  def clear():
    GPIO.output(DATA, 0)

    for x in range(0, 8):
      GPIO.output(CLOCK, 0)
      GPIO.output(CLOCK, 1)  
      GPIO.output(CLOCK, 0)  

    latch()

  # Push bit into the shift register
  def inputBit(inputValue):
    GPIO.output(DATA, inputValue)
    tick()

  # Push a byte to the shift register
  # Takes a string, by the way:
  #   bytestring = format(numericArr[0], '08b')
  #   outputBits(bytestring)
  #  Then, splits input values into individual values
  def outputBits(inputString):
    bitList = list(inputString)
    bitList = bitList[::-1]

    for bit in bitList:
      bit = int(bit)
      inputBit(bit)
    
    latch()


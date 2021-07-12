import RPi.GPIO as GPIO
import math
import time

class ShiftRegister
  numericArr = [        # Stores the numeric display bytes
  0b10000001,
  0b11101101,
  0b01000011,
  0b01001001,
  0b00101101,
  0b00011001,
  0b00010001,
  0b11001101,
  0b00000001,
  0b00001001
  ]

  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)

  DATA  = 21
  LATCH = 20
  CLOCK = 16

  GPIO.setup(DATA,  GPIO.OUT)
  GPIO.setup(LATCH, GPIO.OUT)
  GPIO.setup(CLOCK, GPIO.OUT)

  # Pulses the latch pin - write the output to data lines
  def latch(self):
    GPIO.output(ShiftRegister.LATCH, 0)
    GPIO.output(ShiftRegister.LATCH, 1)
    GPIO.output(ShiftRegister.LATCH, 0)
    #print("Latched")

  # Pulses clock to shift bits
  def tick(self):
    GPIO.output(ShiftRegister.CLOCK, 0)
    GPIO.output(ShiftRegister.CLOCK, 1)
    GPIO.output(ShiftRegister.CLOCK, 0)

  # Clears all outputs by writing an empty byte
  def clear(self):
    GPIO.output(ShiftRegister.DATA, 0)

    for x in range(0, 8):
      GPIO.output(ShiftRegister.CLOCK, 0)
      GPIO.output(ShiftRegister.CLOCK, 1)  
      GPIO.output(ShiftRegister.CLOCK, 0)  

    self.latch()

  # Push bit into the shift register
  def inputBit(self, inputValue):
    GPIO.output(ShiftRegister.DATA, inputValue)
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

  def tempSequencer(self, seqStep):
    #divideStep = seqStep / 16    #TODO: figure out why this doesn't work
    #TODO: figure out how to do file logging
    #TODO: Figure out a better way to handle inputs and outputs (shouldnt be doing this in this file, probably)

    try: 
      ledStep = math.floor(seqStep / 4)
    except ZeroDivisionError:
      ledStep = 0

    disabledSegments = "1" * (5 * 8)

    ledString = ""
    
    for i in range(0, 16):
      ledString += "1" if i == ledStep else "0"

    # outputString = disabledSegments + ledString
    # self.outputBits(outputString)
    return ledString

  def createBPMstring(self, gv):
    bpm = format(gv.bpm)
    while len(bpm) < 3:
      bpm = "0" + bpm

    bpmString = ""

    for i in range(3):
      bpmString = bpmString + format(numericArr[int(bpm[i])], '08b')

    return bpmString  

  def createOutputString(self, gv):
    sequencerString = tempSequencer(self, gv.seqstep)
    bpmString = createBPMstring(self, gv)

    outputString = bpmString + "0000000000000000" + sequencerString
    outputBits(self, outputString)


  # TODO: write function that creates the bitstring thats to be sent
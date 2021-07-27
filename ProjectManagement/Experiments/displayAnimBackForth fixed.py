import RPi.GPIO as GPIO
import time

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
DATA  = 21
LATCH = 20
CLOCK = 16
#BTITERATE = 12
GPIO.setup(DATA,  GPIO.OUT)
GPIO.setup(LATCH, GPIO.OUT)
GPIO.setup(CLOCK, GPIO.OUT)
#GPIO.setup(BTITERATE, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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

# Clears all outputs by writing empty byte
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
#   Split input alues into individual values
def outputBits(inputString):
  bitList = list(inputString)
  bitList = bitList[::-1]

  for bit in bitList:
    bit = int(bit)
    inputBit(bit)
  
  latch()

clear() # Makes sure we're clear before main loop

# Setup
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

outputString = "01111111" + "11111111" * 4
outputList = list(outputString)
heading = 0

while True: 
  i = outputList.index('0')     # Get index
  if heading == 0:
    if i+1 == len(outputList):    # Make sure we don't go out of bounds
      outputList[-1:] = '1'         # If we do go out of bounds, reset last to 1
      outputList[-2:] = '0'           # ...and set first to 0 TODO: needs to be inverted for regular led, calculate pos after 3 bytes
      outputList.append('1')
      heading = 1
    else:
      if i <= 40:
        outputList[i] = '1'           # Flip current 'bit'
        outputList[i+1] = '0'         # Flip next 'bit'
      else:
        outputList[i] = '0'
        outputList[i+1] = '1'
  else:
    if i == 0:
      heading = 0
    else:
      outputList[i] = '1'
      outputList[i-1] = '0'

  outputString = ""
  outputString = outputString.join(outputList)

  print(outputString)
  outputBits(outputString)  

  time.sleep(0.05)  


#bytestring = format(value, '08b')
#outputBits(bytestring)

  # NUMBERS
  # 0 = on (pulled to ground), 1 = off
  # 0 0b10000001
  # 1 0b11101101
  # 2 0b01000011
  # 3 0b01001001
  # 4 0b00101101
  # 5 0b00011001
  # 6 0b00010001
  # 7 0b11001101
  # 8 0b00000001
  # 9 0b00001001
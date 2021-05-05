import RPi.GPIO as GPIO
import time
import math

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

  for x in range(0, 64):
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

# https://tutorialedge.net/compsci/bit-manipulation-for-beginners/
# Can be used for setting individual bits
def set_bit(position, binary):
  ## Create a bit mask based on the
  ## position passed in
  ## produces '10000' if we pass in position=4
  ## our bit in the '4th' position is set to 1
  bit_mask = 1 << position
  ## return our binary string or-ed with our mask
  return bit_mask | binary

clear() # Makes sure we're clear before main loop

# Setup
numericArr = [        # Stores the numeric display bytes
  0b10000000,
  0b11101100,
  0b01000010,
  0b01001000,
  0b00101100,
  0b00011000,
  0b00010000,
  0b11001100,
  0b00000000,
  0b00001000
]

byteArray = [0, 0, 0, 0, 0]
outputByteString = ""

for x in range(0, 5):
  if x < 3:
    byteArray[x] = 0b01010101
  else:
    byteArray[x] = 0b10101010

#bytestring = format(numericArr[0], '08b')
#outputBits(bytestring)

flip = 0

while True:
  for byte in byteArray:
    if flip == 0:
      byte = byte<<1
      flip = 1
    else:
      byte = byte>>1
      flip = 0
      
    inputByteString = format(byte, '08b')
    outputByteString +=  inputByteString 
    
  print(outputByteString)
  outputBits(outputByteString)

  outputByteString = ""

  time.sleep(0.5)


#bytestring = format(value, '08b')
#outputBits(bytestring)

  # NUMBERS
  # 0 = on (pulled to ground), 1 = off
  # 0 0b10000000
  # 1 0b11101100
  # 2 0b01000010
  # 3 0b01001000
  # 4 0b00101100
  # 5 0b00011000
  # 6 0b00010000
  # 7 0b11001100
  # 8 0b00000000
  # 9 0b00001000
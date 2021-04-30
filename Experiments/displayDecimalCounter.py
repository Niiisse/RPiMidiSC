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

firstDigit = 0        # 10s num
secondDigit = 0       # 1s num
bytestring = format(numericArr[0], '08b')
outputBits(bytestring)

#debounceToc = 0

while True:

  if secondDigit < 9:                   # For clamping
    secondDigit += 1
  else:
    secondDigit = 0
    firstDigit += 1

  if firstDigit > 9:
    firstDigit = 0

  firstBytestring = format(numericArr[firstDigit], '08b')
  secondBytestring = format(numericArr[secondDigit], '08b')
  outputBytestring = firstBytestring + secondBytestring
  print(firstBytestring, secondBytestring, outputBytestring)

  outputBits(outputBytestring)

  time.sleep(0.5)


#bytestring = format(value, '08b')
#outputBits(bytestring)

  # NUMBERS
  # 0 = on (pulled to ground), 1 = off
  # 0 100000000
  # 1 0b11101100
  # 2 0b01000010
  # 3 0b01001000
  # 4 0b00101100
  # 5 0b00011000
  # 6 0b00010000
  # 7 0b11001100
  # 8 0b00000000
  # 9 0b00001000

import RPi.GPIO as GPIO
import time

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
DATA  = 21
LATCH = 20
CLOCK = 16
BTITERATE = 12
GPIO.setup(DATA,  GPIO.OUT)
GPIO.setup(LATCH, GPIO.OUT)
GPIO.setup(CLOCK, GPIO.OUT)
GPIO.setup(BTITERATE, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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

thirdDigit = 0      # 100s num
secondDigit = 0       # 10s num
firstDigit = 0       # 1
bytestring = format(numericArr[0], '08b')
outputBits(bytestring)

fillerString = "11111111111111110000000000000000"

strInput = input("Sleep time: ")
sleeptime = float(strInput)

while True:
  if thirdDigit < 9:
    thirdDigit += 1 
  else:
    thirdDigit = 0
    secondDigit += 1

  if secondDigit > 9:                   # For clamping
    secondDigit = 0
    firstDigit += 1

  if firstDigit > 9:
    firstDigit = 0

  firstBytestring = format(numericArr[firstDigit], '08b')
  secondBytestring = format(numericArr[secondDigit], '08b')
  thirdBytestring = format(numericArr[thirdDigit], '08b')
  outputBytestring = firstBytestring + secondBytestring + thirdBytestring + fillerString

  
  print(firstBytestring, secondBytestring, thirdBytestring)

  outputBits(outputBytestring)

  time.sleep(sleeptime)


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
import RPi.GPIO as GPIO
from Debounce import Debounce
import time

class BPMvars:
  thirdDigit = 0          # 100s num
  secondDigit = 0         # 10s num
  firstDigit = 0          # 1
  fillerString = "11111111111111110000000000000000"


# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
DATA  = 21
LATCH = 20
CLOCK = 16
BT_BPM_PLUS = 12
BT_BPM_MIN = 6
GPIO.setup(DATA,  GPIO.OUT)
GPIO.setup(LATCH, GPIO.OUT)
GPIO.setup(CLOCK, GPIO.OUT)
GPIO.setup(BT_BPM_PLUS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BT_BPM_MIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


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

  #TODO: WRITE PROPER CODE FOR THIS (arrays)

  #TODO: for debouncing, make small state machine that differs between just pressed (increment one); after *1* second 
  #  (increment 2 or more) and long pressed (increment a LOT) - add 4 or 5 more states or figure out a function that does it
  #   depending on the amount of time that has passed (harder but fancier; should cap that though)
  #   use time.time
  #   TODO: TURN IT INTO A CLASS!
  # good luck, future me!

def bpmUp():
  BPMvars.thirdDigit += 1

  if BPMvars.thirdDigit > 9:
    BPMvars.thirdDigit = 0
    BPMvars.secondDigit += 1

  if BPMvars.secondDigit > 9:                   
    BPMvars.secondDigit = 0
    BPMvars.firstDigit += 1

  if BPMvars.firstDigit > 9:
    BPMvars.firstDigit = 0

  handleOutput()

def bpmDown():
  BPMvars.thirdDigit -= 1

  if BPMvars.thirdDigit < 0:
    BPMvars.thirdDigit = 9
    BPMvars.secondDigit -= 1

  if BPMvars.secondDigit < 0:                   
    BPMvars.secondDigit = 9
    BPMvars.firstDigit -= 1

  if BPMvars.firstDigit < 0:
    BPMvars.firstDigit = 9

  handleOutput()

def handleOutput():
  firstBytestring = format(numericArr[BPMvars.firstDigit], '08b')
  secondBytestring = format(numericArr[BPMvars.secondDigit], '08b')
  thirdBytestring = format(numericArr[BPMvars.thirdDigit], '08b')
  outputBytestring = firstBytestring + secondBytestring + thirdBytestring + BPMvars.fillerString

  #print(firstBytestring, secondBytestring, thirdBytestring)

  outputBits(outputBytestring)

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

bytestring = "1" * 40 + "0" * 16      # For turning off display at start
outputBits(bytestring)

bpmPlusDb = Debounce()
bpmMinDb = Debounce()

tic = time.time()

startingValue = 120
for i in range(startingValue):
  bpmUp()

print("Initialized with BPM: ", str(startingValue))

while True:
  
  # Handles BPM PLUS input
  btPlus = not GPIO.input(BT_BPM_PLUS)

  if btPlus:
    bpmPlusDb.setState(btPlus)
    if bpmPlusDb.checkDebounce():
      bpmUp()

  elif not btPlus and bpmPlusDb.btDown:
    bpmPlusDb.setState(btPlus)
  
  # Handles BPM MINUS input
  btMin = not GPIO.input(BT_BPM_MIN)            # Gets GPIO button input state
  
  if btMin:
    bpmMinDb.setState(btMin)
    if bpmMinDb.checkDebounce():
      bpmDown()

  elif not btMin and bpmMinDb.btDown:
    bpmMinDb.setState(btPlus)

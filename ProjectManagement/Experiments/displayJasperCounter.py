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

jasperArray = [ 
  0b10000001,
  0b10110111,
  0b00011001,
  0b10010011, 
  0b01110001
] #

outputByteString = ""

while True:
  #format(string, '08b')

  # Clear the displays
  for x in range(0, 5):
    outputByteString = outputByteString + "11111111"
    #print(outputByteString)

    if x == 13:
      outputBits(fullyEmptyByte)
      time.sleep(sleeptime)
  outputBits(outputByteString)
  outputByteString = ""
  emptyByte = "11111111"
  fullyEmptyByte = emptyByte + emptyByte + emptyByte + emptyByte + emptyByte 
  fullyFullByte = ""
  for x in range(0,5):
    fullyFullByte = fullyFullByte + str(format(jasperArray[x], '08b'))

  sleeptime = 0.175

  for x in range(0, 16):
    if x == 0:
      outputByteString = str(format(jasperArray[0], '08b') + emptyByte + emptyByte + emptyByte + emptyByte)
      outputBits(outputByteString)
      time.sleep(sleeptime)

    if x == 1:
      outputByteString = emptyByte + str(format(jasperArray[1], '08b') + emptyByte + emptyByte + emptyByte)
      outputBits(outputByteString)
      time.sleep(sleeptime)
    
    if x == 2:
      outputByteString = emptyByte + emptyByte + str(format(jasperArray[2], '08b') + emptyByte + emptyByte)
      outputBits(outputByteString)
      time.sleep(sleeptime)

    if x == 3:
      outputByteString = emptyByte + emptyByte + emptyByte + str(format(jasperArray[3], '08b') + emptyByte)
      outputBits(outputByteString)
      time.sleep(sleeptime)

    if x == 4:
      outputByteString = emptyByte + emptyByte + emptyByte + emptyByte + str(format(jasperArray[4], '08b'))
      outputBits(outputByteString)
      time.sleep(sleeptime)

    if x == 5:
      outputByteString = emptyByte + emptyByte + emptyByte + str(format(jasperArray[3], '08b') + emptyByte)
      outputBits(outputByteString)
      time.sleep(sleeptime)    

    if x == 6:
      outputByteString = emptyByte + emptyByte + str(format(jasperArray[2], '08b') + emptyByte + emptyByte)
      outputBits(outputByteString)
      time.sleep(sleeptime)  

    if x == 7:
      outputByteString = emptyByte + str(format(jasperArray[1], '08b') + emptyByte + emptyByte + emptyByte)
      outputBits(outputByteString)
      time.sleep(sleeptime)

    if x == 8:
      outputByteString = str(format(jasperArray[0], '08b') + emptyByte + emptyByte + emptyByte + emptyByte)
      outputBits(outputByteString)
      time.sleep(sleeptime)

    if x == 9:
      outputBits(fullyEmptyByte)
      time.sleep(sleeptime)
      
    if x == 10:
      outputBits(fullyFullByte)
      time.sleep(sleeptime)

    if x == 11:
      outputBits(fullyEmptyByte)
      time.sleep(sleeptime)

    if x == 12:
      outputBits(fullyFullByte)
      time.sleep(sleeptime)

    if x == 13:
      outputBits(fullyEmptyByte)
      time.sleep(sleeptime)

    if x == 14:
      outputBits(fullyFullByte)
      time.sleep(sleeptime)

    if x == 15:
      outputBits(fullyEmptyByte)
      time.sleep(sleeptime)

    print(outputByteString)

  

  print(outputByteString)
  outputBits(outputByteString)

  outputByteString = ""

  #time.sleep(sleeptime)


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
  # 9 0b00001001
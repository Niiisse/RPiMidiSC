import RPi.GPIO as GPIO
import time

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
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

# Clears all outputs by writing empty byte
def clear():
  GPIO.output(DATA, 0)

  for x in range(0, 8):
    GPIO.output(CLOCK, 0)
    GPIO.output(CLOCK, 1)  
    GPIO.output(CLOCK, 0)  

  print("Cleared")
  latch()

# Push bit into the shift register
def inputBit(inputValue):
  GPIO.output(DATA, inputValue)
  #print("Put ," inputValue, " in")
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

interrupted = False
value = 0b11111110

bytestring = format(value, '08b')
outputBits(bytestring)

#  for x in range(0, 12):
#    bytestring = format(value, '08b')
#    outputBits(bytestring)
#    print(bytestring)

#    if x < 6:
#      value >>= 1
#
#    else:
#      value <<=1

#    time.sleep(0.5)

  #bote = input("Byte: ")
  #outputBits(bote)
  

  # 1 0b11101100
  # 2 0b01000010
  # 3 0b01001000
  # 4 0b00101100
  # 5 0b00011000
  # 6 0b00010000
  # 7 0b11001101
  # 8
  # 9 0b00001001
  # 10
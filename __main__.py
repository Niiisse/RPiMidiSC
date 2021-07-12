import Software.UserInterface as ui
import Software.GlobalVars
import config
import math
import sys

# Check whether the hardware interface is enabled or disabled in config
# I added this to make local debugging without hardware easier
if config.general['hardware_enabled']:
  import Hardware.HardwareInterface as HWi
  sr = HWi.ShiftRegister()


print("RPiMidiSC")
ui.startUI()
gv = Software.GlobalVars.GlobalVars()  #

# FIXME: get this temp bullshit out of here

def tempSequencer():
  #divideStep = seqStep / 16    #TODO: figure out why this doesn't work
  #TODO: figure out how to do file logging
  #TODO: Figure out a better way to handle inputs and outputs (shouldnt be doing this in this file, probably)

  try: 
    ledStep = math.floor(gv.seqstep / 4)
  except ZeroDivisionError:
    ledStep = 0

  ledString = ""
  
  for i in range(0, 16):
    ledString += "1" if i == ledStep else "0"

  # outputString = disabledSegments + ledString
  # self.outputBits(outputString)
  return ledString

def createBPMstring(bpmVal):
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

  bpm = format(bpmVal)
  while len(bpm) < 3:
    bpm = "0" + bpm

  bpmString = ""

  for i in range(3):
    bpmString = bpmString + format(numericArr[int(bpm[i])], '08b')

  return bpmString  

createPatternString():
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

  patternStep = format(gv.patternStep)
  while len(patternStep) < 2:
    patternStep = "0" + patternStep

  patternString = ""

  for i in range(3):
    patternString = patternString + format(numericArr[int(patternStep[i])], '08b')


  return patternString

def createOutputString(bpm):
  sequencerString = tempSequencer()
  bpmString = createBPMstring(bpm)
  patternString = createPatternString()

  outputString = bpmString + patternString + sequencerString
  #print(outputString)
  return outputString


while (True):
  try_quit = ui.update_ui()   # Runs UI loop; returns 0 normally
  if try_quit == "quit":           # However, it returns 1 when q is pressed...  
    ui.restoreScreen()      
    sys.exit(0)               # ...signalling us to exit.
  if try_quit == "reset":
    ui.resetScreen()
    ui.startUI()


  if config.general['hardware_enabled']:
    #TODO: optimize; only call on change?
    bpmlocal = gv.bpm
    bitString = createOutputString(bpmlocal)
    sr.outputBits(bitString)


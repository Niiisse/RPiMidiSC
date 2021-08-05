import Modules.UserInterface as ui

import config
import sys
from pprint import pprint

# Check whether the hardware interface is enabled or disabled in config

if config.general['hardware_enabled']:
  import Modules.HardwareInterface as HWi
  sr = HWi.ShiftRegister()

# Program start

print("RPiMidiSC")
ui.startUI()
#gv = Modules.GlobalVars.GlobalVars()  #

while (True):
  # Main program loop

  # Runs UI (which, admittedly, runs most of the program)
  # UI can return 0 for graceful exit - necessary because Curses will fuck up the console otherwise
  # UI can also return 1 for reset; this resets Curses, but not the program state
  # If none of that happens, it returns the bytestring which can be sent to the hardware interface

  uiResult = ui.updateUi()   
  
  if uiResult == "quit":           
    ui.restoreScreen()

    # Some debugging code for sequencer object
    # sequencer = ui.getSequencer()
    # for i in range(sequencer.seqstepmax):
    #   print(sequencer.patterns[1].patternSteps[i].getState())
    # pprint(vars(ui.getSequencer()))
    #pprint(vars(sequencer.patterns[1]))

    sys.exit(0)     
  
  elif uiResult == "reset":
    ui.resetScreen()
    ui.startUI()
  
  elif config.general['hardware_enabled']:
    sr.outputBits(uiResult)
    
# def sendByteString(outputByteString):
#   sr.outputBits(outputByteString)
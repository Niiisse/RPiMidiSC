import Modules.UserInterface as ui
import Modules.Midi as Midi

import config
import sys
from pprint import pprint

# Check whether the hardware interface is enabled or disabled in config

if config.general['hardware_enabled']:
  import Modules.HardwareInterface as HWi
  sr = HWi.ShiftRegister()

# Program start
#midi = Midi.Midi()

print("RPiMidiSC")
ui.startUI()

while (True):
  # Main program loop

  # Runs UI (which, admittedly, runs most of the program)
  # UI can return 0 for graceful exit - necessary because Curses will fuck up the console otherwise
  # UI can also return 1 for reset; this resets Curses, but not the program state
  # If none of that happens, it returns the bytestring which can be sent to the hardware interface

  uiResult = ui.updateUi()   
  
  if uiResult == "quit":           
    ui.restoreScreen()
    # TODO: gracefully exit MIDI too

    sys.exit(0)     
  
  elif uiResult == "reset":
    ui.resetScreen()
    ui.startUI()

  
  elif config.general['hardware_enabled']:
    sr.outputBits(uiResult)
    
# def sendByteString(outputByteString):
#   sr.outputBits(outputByteString)
import Software.UserInterface as ui
import Software.GlobalVars
import config
import sys

# Check whether the hardware interface is enabled or disabled in config

if config.general['hardware_enabled']:
  import Hardware.HardwareInterface as HWi
  sr = HWi.ShiftRegister()

# Program start

print("RPiMidiSC")
ui.startUI()
gv = Software.GlobalVars.GlobalVars()  #

while (True):
  # Main program loop

  # Runs UI (which, admittedly, runs most of the program)
  # UI can return 0 for graceful exit - necessary because Curses will fuck up the console otherwise
  # UI can also return 1 for reset; this resets Curses, but not the program state
  # If none of that happens, it returns the bytestring which can be sent to the hardware interface

  uiResult = ui.updateUi()   

  print(uiResult)

  if uiResult == "quit":           
    ui.restoreScreen()      
    sys.exit(0)     
  
  elif uiResult == "reset":
    ui.resetScreen()
    ui.startUI()
  
  elif config.general['hardware_enabled']:
    sr.outputBits(uiResult)
    
# def sendByteString(outputByteString):
#   sr.outputBits(outputByteString)
import UserInterface as ui
#import HardwareInterface as HWi
import sys


print("RPiMidiSC")
ui.startUI()

while (True):
  try_quit = ui.update_ui()   # Runs UI loop; returns 0 normally
  if try_quit == 1:           # However, it returns 1 when q is pressed...        
    sys.exit(0)               # ...signalling us to exit.

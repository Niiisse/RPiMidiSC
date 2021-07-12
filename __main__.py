import Software.UserInterface as ui
import Software.GlobalVars
import config
import sys

# Check whether the hardware interface is enabled or disabled in config
# I added this to make local debugging without hardware easier
if config.general['hardware_enabled']:
  import Hardware.HardwareInterface as HWi
  sr = HWi.ShiftRegister()


print("RPiMidiSC")
ui.startUI()
gv = Software.GlobalVars.GlobalVars()  #


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

    #sr.tempSequencer(gv.seqstep)
    sr.createOutputString(sr, gv.seqstep, gv.bpm)
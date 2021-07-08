import UserInterface as ui
import GlobalVars
import config
import sys

# Check whether the hardware interface is enabled or disabled in config
# I added this to make local debugging without hardware easier
if config.general['hardware_enabled']:
  import HardwareInterface as HWi
  sr = HWi.ShiftRegister()


print("RPiMidiSC")
ui.startUI()
gv = GlobalVars.GlobalVars()  #


while (True):
  try_quit = ui.update_ui()   # Runs UI loop; returns 0 normally
  if try_quit == 1:           # However, it returns 1 when q is pressed...  
    ui.restoreScreen()      
    sys.exit(0)               # ...signalling us to exit.
  if try_quit == 2:
    ui.resetScreen()
    ui.startUI()


  if config.general['hardware_enabled']:
    seqstep = gv.getSeqstep()
    sr.tempSequencer(seqstep)

#TODO: call HWi.CreateBitString();
from rich.layout import Layout
from rich.live import Live
import Ui.UserInterface as ui
# import Modules.Midi as Midi

import config
import time
import sys

# Check whether the hardware interface is enabled or disabled in config

if config.general['hardware_enabled']:
  import Hardware.HardwareInterface as HWi
  sr = HWi.ShiftRegister(21, 20, 16)

# Program start

print("RPiMidiSC")

def saveLoadAnim():
  outputString = config.misc['hw_off_string']

  for i in range(4):
    outputList = list(outputString)

    for bit in range(len(outputList)):
      if outputList[bit] == '0':
        outputList[bit] = '1'
      else:
        outputList[bit] = '0'

      outputString = ""
      outputString = outputString.join(outputList)
      sr.outputBits(outputString)

    time.sleep(0.05)

layout = Layout(name="root")

with Live(layout, screen=True, refresh_per_second=30) as live:
  while (True):
    # Main program loop

    # UI can return 0 for graceful exit - necessary because Curses will fuck up the console otherwise
    # UI can also return 1 for reset; this resets Curses, but not the program state
    # If none of that happens, it returns the bytestring which can be sent to the hardware interfaces

    layout["root"].update(ui.generateUi())

    uiResult = ui.updateUi()

    if uiResult == "saveAnim":
      saveLoadAnim()

    elif uiResult == "quit":
      val = ui.safeExit()
      if config.general['hardware_enabled']:
        sr.outputBits(val)
      sys.exit(0)

    elif config.general['hardware_enabled']:
      sr.outputBits(uiResult)       # Sequencer info; Note control modules

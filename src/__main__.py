import sys
from rich.live import Live

from Hardware import InputInterface
from Sequencing.Sequencer import Sequencer
from Hardware.OutputInterface import OutputInterface
from Ui.NewUserInterface import NewUi

sequencer = Sequencer()
outputInterface = OutputInterface()
ui = NewUi()

sequencer.togglePlay() # FIXME: FOR TESTING

running = True

with Live(screen=True, refresh_per_second=30) as display:
  while running:
    try:
      if sequencer.update():
        outputString = outputInterface.generateOutputString(sequencer)
        outputInterface.outputData(outputString)
        display.update(ui.updateUi(sequencer, outputString))

      sequencer.processInput(InputInterface.readInputData())

    except KeyboardInterrupt:
      running = False

    except:
      # TODO: try to backup save
      outputInterface.outputCrash()
      sys.exit(1)

outputInterface.outputShutdown()
sys.exit(0)









# Check whether the hardware interface is enabled or disabled in config
# if config.general['hardware_enabled']:
#   import Hardware.HardwareInterface as HWi
#   sr = HWi.ShiftRegister(21, 20, 16)

# Program start

# def saveLoadAnim():
#   outputString = config.misc['hw_off_string']

#   for i in range(4):
#     outputList = list(outputString)

#     for bit in range(len(outputList)):
#       if outputList[bit] == '0':
#         outputList[bit] = '1'
#       else:
#         outputList[bit] = '0'

#       outputString = ""
#       outputString = outputString.join(outputList)
#       sr.outputBits(outputString)

#     time.sleep(0.05)

# layout = Layout(name="root")

# with Live(layout, screen=True, refresh_per_second=30) as live:
#   while (True):
#     # Main program loop

#     # UI can return 0 for graceful exit - necessary because Curses will fuck up the console otherwise
#     # UI can also return 1 for reset; this resets Curses, but not the program state
#     # If none of that happens, it returns the bytestring which can be sent to the hardware interfaces

#     layout["root"].update(ui.generateUi())

#     uiResult = ui.updateUi()

#     if uiResult == "saveAnim":
#       saveLoadAnim()

#     elif uiResult == "quit":
#       val = ui.safeExit()
#       if config.general['hardware_enabled']:
#         sr.outputBits(val)
#       sys.exit(0)

#     elif config.general['hardware_enabled']:
#       sr.outputBits(uiResult)       # Sequencer info; Note control modules

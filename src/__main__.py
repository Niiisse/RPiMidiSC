import sys
# from rich.live import Live


from Hardware import InputInterface
from Sequencing.Sequencer import Sequencer
from Hardware.OutputInterface import OutputInterface
from Ui.NewUserInterface import NewUi

exception = None

sequencer = Sequencer()
outputInterface = OutputInterface()
ui = NewUi()

running = True

# with Live(screen=True, refresh_per_second=30) as display:
while running:
  try:
    sequencer.update()
    outputString = outputInterface.generateOutputString(sequencer)
    outputInterface.outputData(outputString)

    # display.update(ui.updateUi(sequencer, outputString))

    sequencer.processInput(InputInterface.readInputData())

  except KeyboardInterrupt:
    running = False

  except Exception as e:
    # TODO: try to backup save
    outputInterface.outputCrash()
    print(str(e))

    sys.exit(1)

outputInterface.outputShutdown()
# midi disable
sys.exit(0)


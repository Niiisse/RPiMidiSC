import sys
import time

from Hardware import InputInterface
from Sequencing.Sequencer import Sequencer
from Hardware.OutputInterface import OutputInterface
from Ui.NewUserInterface import NewUi

exception = None

sequencer = Sequencer()
outputInterface = OutputInterface()
ui = NewUi()

running = True

def tickTimer():
    # 'Ticks' timer; sets new timestamp for comparison

    sequencer.tic = time.perf_counter()


def update() -> None:
    """ Handles sequencer's timer
    Responsible for stepping, makes sure we don't infinitely tick the timer """

    if sequencer.playing:
        if sequencer.timerShouldTick:
            sequencer.timerShouldTick = False
            tickTimer()

        # Has enough time gone by for us to tick?
        # " if current time - last tic time > bpm time" ...
        # 60 / bpm for changing bpm to bps; / 4 for sequencer spacing purposes

        if time.perf_counter() - sequencer.tic > (60 / sequencer.sets[sequencer.setIndex].bpm / 4):
            sequencer.sequencerStep()
            outputString = outputInterface.generateOutputString(sequencer)
            outputInterface.outputData(outputString)

            sequencer.processInput(InputInterface.readInputData())
            sequencer.timerShouldTick = True



while running:
    try:
        update()

    except KeyboardInterrupt:
        running = False

    except Exception as e:
        # TODO: try to backup save
        outputInterface.outputCrash()
        print(str(e))

        sys.exit(1)

outputInterface.outputShutdown()  # midi disable
sys.exit(0)



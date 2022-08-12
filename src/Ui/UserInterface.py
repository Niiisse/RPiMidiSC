import config

from rich.panel import Panel

# from Hardware import Input
from Hardware import Blink
from Sequencing import Sequencer

# User Interface class
#
# Handles, well, user interface. Reports program state back to main with a return.

class Ui:
    app_version = config.general['version']
    outputByteString = "no data"

    patternMode = config.pattern['patternMode']
    patternAmount = config.pattern['patternAmount']

    # sequencer = None

    blink = Blink.Blink(config.general['blinkTime'])
    # sequencer = Sequencer.Sequencer(config.pattern['patternAmount'],
                                    # config.sequencer['seqstepmax'],
                                    # config.sequencer['seqstepsize'],
                                    # config.general['midiEnabled'],
                                    # config.sequencer['previewNoteDuration'])

def updateUi(sequencer: Sequencer.Sequencer):
    # Main UI loop. Handles inputs, then updates windows

    clampPatternStepping(sequencer)
    clampPendingStepping(sequencer)

    # Ui.sequencer.checkPreviewNotesOff()

    # Generate output bytestring, process inputs for next frame
    # pass outputByteString to processInput to return the bytestring to main.py, assuming no other
    # events have priority.

    # uiPanel

    # Ui.outputByteString = createOutputString(sequencer)
    return processInput(Ui.outputByteString, sequencer)


def generateUi():
    return Panel("Test!")

##
## UI Creation and Drawing / Updating
##

def clampPatternStepping(sequencer):
    # TODO: move to sequencer
    # Clamps pattern step

    if sequencer.patternIndex > sequencer.patternAmount:
        sequencer.patternIndex = 1
    elif sequencer.patternIndex < 1:
        sequencer.patternIndex = Ui.patternAmount


def clampPendingStepping(sequencer):
    # TODO: move to sequencer
    # Calculate pending pattern stepping. Basically a fancy clamp

    if sequencer.patternChange != 0:
        if sequencer.patternChange > sequencer.patternAmount - sequencer.patternIndex:
            sequencer.patternChange -= sequencer.patternAmount

        if sequencer.patternChange + sequencer.patternIndex < 1:
            sequencer.patternChange += sequencer.patternAmount

    sequencer.pendingPattern = sequencer.patternIndex + sequencer.patternChange

def convertDecimalToByteString(decimal):
    """ Creates outputbytestring. """

    numericArr = [  # Stores the numeric display bytes
        0b10000001,  # 0
        0b11101101,  # 1
        0b01000011,  # 2
        0b01001001,  # 3
        0b00101101,  # 4
        0b00011001,  # 5
        0b00010001,  # 6
        0b11001101,  # 7
        0b00000001,  # 8
        0b00001001,  # 9
        0b00000101,  # 10 / A
        0b00110001,  # 11 / b
        0b01110011,  # 12 / C
        0b01100001,  # 13 / d
        0b00010011,  # 14 / E
        0b00010111  # 15 / F
    ]

    byteString = format(numericArr[decimal], '08b')

    return byteString


def convertDecimalToNote(decimal):
    """ Converts note number to actual note """

    noteArr = [  # Stores the numeric display bytes
        0b01111110,  # -
        0b01110010,  # C
        0b01110011,  # C#
        0b01100000,  # D
        0b01100001,  # D#
        0b00010010,  # E
        0b00010110,  # F
        0b00010111,  # F#
        0b10010000,  # G
        0b10010001,  # G#
        0b00000100,  # A
        0b00000101,  # A#
        0b00110000,  # B
    ]

    byteString = format(noteArr[decimal], '08b')

    return byteString


def binarySaveCounter(index: int) -> str:
    """ Convert save index decimal to LED output string """

    saveArr = [
        0b0001,  # 1
        0b0010,  # 2
        0b0011,  # 3
        0b0100,  # 4
        0b0101,  # 5
        0b0110,  # 6
        0b0111,  # 7
        0b1000,  # 8
        0b1001,  # 9
        0b1010,  # 10
        0b1011,  # 11
        0b1100,  # 12
        0b1101,  # 13
        0b1110,  # 14
        0b1111,  # 15
        0b0000  # 16
    ]

    return format(saveArr[index], '04b')

# def safeExit():
#     """ program is asked to exit, do so properly """

#     # restoreScreen()
#     sequencer.midiInterface.cleanUp()

#     return config.misc['hw_off_string']

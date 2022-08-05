import config
from rich.panel import Panel

from Hardware import Input
from Hardware import Blink
from Sequencing import Sequencer


# User Interface class
#
# Handles, well, user interface. Reports program state back to main with a return.

class Ui:
    app_version = config.general['app_version']
    outputByteString = "no data"

    patternMode = config.pattern['patternMode']
    patternAmount = config.pattern['patternAmount']

    # sequencer = None

    blink = Blink.Blink(config.general['blinkTime'])
    sequencer = Sequencer.Sequencer(config.pattern['patternAmount'], 
                                    config.sequencer['seqstepmax'],
                                    config.sequencer['seqstepsize'],
                                    config.general['midiEnabled'],
                                    config.sequencer['previewNoteDuration'])

def updateUi():
    # Main UI loop. Handles inputs, then updates windows

    clampPatternStepping(Ui.sequencer)
    clampPendingStepping(Ui.sequencer)

    # Ui.sequencer.checkPreviewNotesOff()

    Ui.sequencer.timer()  # Manages sequencer timer

    # Generate output bytestring, process inputs for next frame
    # pass outputByteString to processInput to return the bytestring to main.py, assuming no other
    # events have priority.

    Ui.outputByteString = createOutputString(Ui.sequencer)
    return processInput(Ui.outputByteString, Ui.sequencer)

    
def generateUi():
  return Panel("Test!")

##
## UI Creation and Drawing / Updating
##

def getSequencer():
    return Ui.sequencer


def processInput(outputByteString, sequencer):
    # Process input events sent by Input
    action = Input.doInput()

    # Reset prepareReset if button has been let go
    if action != "prepareReset" and sequencer.prepareReset == True:
        sequencer.prepareReset = False

        # Quit
    if action == "quit":
        return "quit"

    # Reset
    elif action == "reset":
        return "reset"

    # BPM up & down; clamping
    elif action == "bpmUp":
        if sequencer.sets[sequencer.setIndex].bpm < 999:
            sequencer.sets[sequencer.setIndex].bpm += 1
        else:
            sequencer.sets[sequencer.setIndex].bpm = 1

    elif action == "bpmDown":
        if sequencer.sets[sequencer.setIndex].bpm > 1:
            sequencer.sets[sequencer.setIndex].bpm -= 1
        else:
            sequencer.sets[sequencer.setIndex].bpm = 999


    # Sequencer stepping next & previous; clamping
    # FIXME: Move to Sequencer
    # TODO: NCM
    elif action == "seqStepUp":
        sequencer.seqstep += sequencer.stepSize

        if sequencer.seqstep > sequencer.sequencerSteps - sequencer.stepSize:
            sequencer.seqstep = 0

        sequencer.sets[sequencer.setIndex].patterns[sequencer.patternIndex].steps[sequencer.seqstep].selectedLayer[
            0] = sequencer.lastUsedLayer

    elif action == "seqStepDown":
        # FIXME: move to sequencer
        # TODO: NCM
        sequencer.seqstep -= sequencer.stepSize

        if sequencer.seqstep < 0:
            sequencer.seqstep = sequencer.sequencerSteps - sequencer.stepSize

        # Set last used layer as active layer
        sequencer.sets[sequencer.setIndex].patterns[sequencer.patternIndex].steps[sequencer.seqstep].selectedLayer[
            0] = sequencer.lastUsedLayer


    # Pattern Stepping
    elif action == "patternStepUp":
        if sequencer.playing:
            sequencer.patternChange += 1
        else:
            sequencer.patternUp()

    elif action == "patternStepDown":
        if sequencer.playing:
            sequencer.patternChange -= 1
        else:
            sequencer.patternDown()

    # Pattern Editing
    elif action == "patternEdit":
        sequencer.toggleEditMode()

    # Pattern mode switch
    elif action == "togglePatternMode":
        sequencer.togglePatternMode()

    elif action == "toggleStep":
        sequencer.sets[sequencer.setIndex].patterns[sequencer.patternIndex].steps[sequencer.seqstep].toggleStep()

    # Play / Pause toggle
    elif action == "playPause":
        if sequencer.patternEditing == False:
            sequencer.togglePlay()

    # note up/down
    elif action == "noteUp":
        sequencer.noteUp()

    elif action == "noteDown":
        sequencer.noteDown()

    # Note layer
    elif action == "layerUp":
        currentStep = sequencer.sets[sequencer.setIndex].patterns[sequencer.patternIndex].steps[sequencer.seqstep]
        currentStep.layerUp()  # TODO: when multiple NCMs are connected, add second variable to layerUpDown for selecting specific layer
        # (that's why selectedLayer[] is a list; first item = first NCM)

        sequencer.sendMidi(True)
        sequencer.lastUsedLayer = currentStep.selectedLayer[0]

    elif action == "layerDown":
        currentStep = sequencer.sets[sequencer.setIndex].patterns[sequencer.patternIndex].steps[sequencer.seqstep]
        currentStep.layerDown()

        sequencer.sendMidi(True)
        sequencer.lastUsedLayer = currentStep.selectedLayer[0]

    # Note Octave
    elif action == "octaveUp":
        currentStep = sequencer.sets[sequencer.setIndex].patterns[sequencer.patternIndex].steps[sequencer.seqstep]
        currentStep.noteLayers[currentStep.selectedLayer[0]].octaveUp()
        sequencer.lastUsedOctave = currentStep.noteLayers[currentStep.selectedLayer[0]].octave

        sequencer.sendMidi(True)

    elif action == "octaveDown":
        currentStep = sequencer.sets[sequencer.setIndex].patterns[sequencer.patternIndex].steps[sequencer.seqstep]
        currentStep.noteLayers[currentStep.selectedLayer[0]].octaveDown()
        sequencer.lastUsedOctave = currentStep.noteLayers[currentStep.selectedLayer[0]].octave

        sequencer.sendMidi(True)

    # MIDI channel
    elif action == "midiChannelUp":
        currentStep = sequencer.sets[sequencer.setIndex].patterns[sequencer.patternIndex].steps[sequencer.seqstep]
        currentStep.noteLayers[currentStep.selectedLayer[0]].channelUp()

        sequencer.sendMidi(True)
        sequencer.lastUsedMidiChannel = currentStep.noteLayers[
            currentStep.selectedLayer[0]].midiChannel  # TODO: multi NCM support

    elif action == "midiChannelDown":
        currentStep = sequencer.sets[sequencer.setIndex].patterns[sequencer.patternIndex].steps[sequencer.seqstep]
        currentStep.noteLayers[currentStep.selectedLayer[0]].channelDown()

        sequencer.sendMidi(True)
        sequencer.lastUsedMidiChannel = currentStep.noteLayers[
            currentStep.selectedLayer[0]].midiChannel  # TODO: multi NCM support

    # Sustain
    elif action == "toggleSustain":
        currentStep = sequencer.sets[sequencer.setIndex].patterns[sequencer.patternIndex].steps[sequencer.seqstep]
        currentStep.noteLayers[currentStep.selectedLayer[0]].toggleSustain()

    # Arm
    elif action == "toggleArm":
        currentStep = sequencer.sets[sequencer.setIndex].patterns[sequencer.patternIndex].steps[sequencer.seqstep]
        currentStep.noteLayers[currentStep.selectedLayer[0]].toggleArm()

    # Save
    elif action == "save":
        sequencer.save(0)

    elif action == "load":
        sequencer.load(0)

    # Sustain
    elif action == "toggleSustain":
        currentStep = sequencer.sets[sequencer.setIndex].patterns[sequencer.patternIndex].steps[sequencer.seqstep]
        currentStep.noteLayers[currentStep.selectedLayer[0]].toggleSustain()

    # save up/down
    elif action == "saveUp":
        sequencer.saveUp()
    # return "saveAnim"

    elif action == "saveDown":
        sequencer.saveDown()
    # return "saveAnim"

    elif action == "setUp":
        if sequencer.playing:
            sequencer.setChange += 1
            Ui.sequencer.clampPendingSetStepping()

        else:
            sequencer.setUp()

    elif action == "setDown":
        if sequencer.playing:
            sequencer.setChange -= 1
            Ui.sequencer.clampPendingSetStepping()

        else:
            sequencer.setDown()

    elif action == "setRepeat":
        sequencer.toggleSetRepeat()

    elif action == "prepareReset":
        if sequencer.canReset:
            sequencer.prepareReset = True

    elif action == "doReset":
        sequencer.reset()

    return outputByteString


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


def createOutputString(sequencer):
    """ Creates output bytestring that can be sent to Hardware Interface """

    if sequencer.prepareReset:
        resetString = config.misc['resetString']
        return Ui.blink.blink(resetString, True)

    else:
        # BPM #

        bpmString = format(sequencer.sets[sequencer.setIndex].bpm)
        bpmOutput = ""

        while len(bpmString) < 3:  # Because format is '090', not '90'
            bpmString = "0" + bpmString

        for i in range(3):  # Sends individual number off to get the bytestring
            tempString = convertDecimalToByteString(int(bpmString[i]))
            bpmOutput = bpmOutput + tempString

        # PATTERN STEP #

        # Decide whether we should show actual step or pending step
        patternStepString = format(sequencer.patternIndex) if sequencer.patternChange == 0 else format(
            sequencer.pendingPattern)

        while len(patternStepString) < 2:
            patternStepString = "0" + patternStepString

        patternStepOutput = ""

        for i in range(2):
            tempString = convertDecimalToByteString(int(patternStepString[i]))
            patternStepOutput = patternStepOutput + tempString

        # Should we blink?
        if sequencer.patternChange != 0:
            patternStepOutput = Ui.blink.blink(patternStepOutput, True)

        # SEQUENCER STEP #

        ledStep = sequencer.seqstep

        ledString = ""
        ledState = ""

        for i in range(sequencer.sequencerSteps):
            # Gon explain this one in detail cus ternary statements can be confusing to read
            # Loop over all steps in current Pattern
            # ledState sets what the potential state is going to be if this is the selected step.
            #
            # If editing:
            #       BLINK current step LED; else
            #       all LEDs ON; disabled steps: LED OFF
            #
            # If playing:
            #       all LEDs OFF, current step: LED ON
            #       pausing: BLINK current LED

            # editing mode
            if sequencer.patternEditing:
                if i == ledStep:
                    ledState = Ui.blink.blink("1", False)
                else:
                    ledState = "1" if sequencer.sets[sequencer.setIndex].patterns[sequencer.patternIndex].steps[
                        i].getState() else "0"

            # playing mode
            else:
                if i == ledStep:
                    if sequencer.sets[sequencer.setIndex].patterns[sequencer.patternIndex].steps[i].getState():
                        ledState = "1" if sequencer.playing == True else Ui.blink.blink("1", False)
                    else:
                        ledState = Ui.blink.blink("1", False) if sequencer.playing == False else "0"
                else:
                    ledState = "0"

            ledString += ledState

        # NOTEMODULE #

        noteString = "11111110"
        layerString = "11111110"
        octaveString = "11111110"
        channelString = "11111111"

        currentStep = sequencer.sets[sequencer.setIndex].patterns[sequencer.patternIndex].steps[sequencer.seqstep]

        noteString = convertDecimalToNote(currentStep.noteLayers[currentStep.selectedLayer[
            0]].note)  # TODO: this 0 would be replaced with i for note control modules
        layerString = convertDecimalToByteString(currentStep.selectedLayer[0])
        channelString = convertDecimalToByteString(currentStep.noteLayers[currentStep.selectedLayer[0]].midiChannel)

        if currentStep.noteLayers[currentStep.selectedLayer[0]].note != 0:
            # Checks whether it should display the values or write - (in case of disabled note)
            octaveString = convertDecimalToByteString(currentStep.noteLayers[currentStep.selectedLayer[0]].octave)

        else:
            octaveString = "01111111"

        # Note layer bit
        layerString = layerString[:-1] + '0'

        if currentStep.checkOtherLayers():
            layerString = layerString[:-1] + '1'

        # Sustain Bit
        if currentStep.noteLayers[currentStep.selectedLayer[0]].sustain:
            octaveString = octaveString[:-1] + '1'
        else:
            octaveString = octaveString[:-1] + '0'

        # Arm Bit
        if currentStep.noteLayers[currentStep.selectedLayer[0]].arm:
            channelString = channelString[:-1] + '1'
        else:
            channelString = channelString[:-1] + '0'

        # PLAY / GENERAL CONTROL BOARD
        gcOutput = list("0000")

        # Green LED ON, red OFF if playing, inverted otherwise
        if sequencer.playing:
            gcOutput[1] = '1'
            gcOutput[2] = '0'
        else:
            gcOutput[1] = '0'
            gcOutput[2] = '1'

        # Yellow LED if patternMode == single
        if sequencer.patternMode == 'single':
            gcOutput[3] = '1'

        # Add 4 bits for SaveIndex
        gcOutputString = "".join(gcOutput) + binarySaveCounter(sequencer.saveIndex)

        # Set display + LED #

        # Decide whether we should show actual setIndex or pending index
        setString = sequencer.setIndex if sequencer.setChange == 0 else sequencer.setPending

        setString = convertDecimalToByteString(setString)

        # Should we blink?
        if sequencer.setChange != 0:
            setString = Ui.blink.blink(setString, True)

        setString = '1' + setString[:-1] if sequencer.setRepeat else '0' + setString[:-1]

        # OUTPUT #
        # 0 = original module (steps, bpm, pattern), note control module(s)
        # 1 = playing board

        output = bpmOutput + patternStepOutput + ledString + noteString + layerString + octaveString + channelString + gcOutputString + setString

        return output


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

def safeExit():
    """ program is asked to exit, do so properly """

    # restoreScreen()
    Ui.sequencer.midiInterface.cleanUp()

    return config.misc['hw_off_string']

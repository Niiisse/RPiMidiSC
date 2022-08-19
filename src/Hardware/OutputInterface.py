import Hardware.Blink as Blink
from Sequencing.Sequencer import Sequencer
import config

class OutputInterface:

  def __init__(self):
    self.hardwareEnabled = False

    if config.general['hardware_enabled']:
      import Hardware.HardwareInterface as HWi
      self.sr = HWi.ShiftRegister(21, 20, 16)
      self.hardwareEnabled = True

    self.blink = Blink.Blink(config.general['blinkTime'])
    self.shutdownString = config.misc['hw_off_string']
    self.crashString = config.misc['hw_crash_string']

  def outputData(self, outputData: str) -> None:
    if self.hardwareEnabled:
      self.sr.outputBits(outputData)

  def outputCrash(self) -> None:
    """ Output crash string to sequencer, if hw enabled """
    if self.hardwareEnabled:
      self.sr.outputBits(self.crashString)

  def outputShutdown(self) -> None:
    """ Output shutdown data to sequencer, if hw enabled """

    if self.hardwareEnabled:
      self.sr.outputBits(self.shutdownString)

  def generateOutputString(self, sequencer: Sequencer) -> str:
    """ Glues all individual outputs together and returns it """

    if sequencer.prepareReset and sequencer.canReset:
      return self.doResetAnim()
    else:
      outputString = ""

      outputString = self.generateTempoData(sequencer.sets[sequencer.setIndex].bpm)
      outputString += self.generatePatternData(sequencer.patternIndex, sequencer.patternChange, sequencer.pendingPattern)
      outputString += self.generateSeqstepData(sequencer.seqstep, sequencer.sets, sequencer.playing, sequencer.setIndex, sequencer.patternIndex, sequencer.sequencerSteps )
      outputString += self.generateNoteControlModuleData(sequencer.sets, sequencer.setIndex, sequencer.patternIndex, sequencer.seqstep)
      outputString += self.generatePlayStatusData(sequencer.playing, sequencer.patternMode, sequencer.saveIndex)
      outputString += self.generateSetData(sequencer.setIndex, sequencer.setChange, sequencer.setPending, sequencer.setRepeat)

      return outputString

  def doResetAnim(self) -> str:
    """ Reset animation """

    outputString = config.misc['resetString']
    return self.blink.blink(outputString, True)

  def generateTempoData(self, bpm: int) -> str:
    """ Creates BPM string """
    bpmString = format(bpm)
    bpmOutput = ""
    tempString = ""

    while len(bpmString) < 3:  # Because format is '090', not '90'
      bpmString = "0" + bpmString

    for i in range(3):  # Sends individual number off to get the bytestring
      tempString = self.convertDecimalToByteString(int(bpmString[i]))

      bpmOutput = bpmOutput + tempString

    return bpmOutput

  def generatePatternData(self,patternIndex: int, patternChange: int, pendingPattern: int) -> str:
    """ Creates pattern string

        Checks whether current or pending pattern should be shown """

    patternStepString = format(patternIndex) if patternChange == 0 else format(
      pendingPattern)

    patternStepOutput = ""

    while len(patternStepString) < 2:
      patternStepString = "0" + patternStepString

      for i in range(2):
        tempString = self.convertDecimalToByteString(int(patternStepString[i]))
        patternStepOutput = patternStepOutput + tempString

        # Should we blink?
        if patternChange != 0:
          patternStepOutput = self.blink.blink(patternStepOutput, True)

    return patternStepOutput

  def generateSeqstepData(self, seqstep: int, sets: list, playing: bool, setIndex: int, patternIndex: int, steps: int ) -> str:
    """ Create seqstep string

        - Loop over all steps in pattern
        - ledState contains data for this step; add to main string.

        If playing: all LEDs 0, LED for current step 1
        If pausing: blink current LED"""

    ledStep = seqstep
    ledString = ""
    ledState = ""

    for i in range(steps):
      if i == ledStep:
        if sets[setIndex].patterns[patternIndex].steps[i].getState():
          ledState = "1" if playing == True else self.blink.blink("1", False)
        else:
          ledState = self.blink.blink("1", False) if playing == False else "0"
      else:
        ledState = "0"

      ledString += ledState

    return ledString

  def generateNoteControlModuleData(self, sets: list, setIndex: int, patternIndex: int, seqstep: int) -> str:
    """ Creates Note Control Module output """

    noteString = "11111110"
    layerString = "11111110"
    octaveString = "11111110"
    channelString = "11111111"

    currentStep = sets[setIndex].patterns[patternIndex].steps[seqstep]

    noteString = self.convertDecimalToNote(currentStep.noteLayers[currentStep.selectedLayer[0]].note)
    layerString = self.convertDecimalToByteString(currentStep.selectedLayer[0])
    channelString = self.convertDecimalToByteString(currentStep.noteLayers[currentStep.selectedLayer[0]].midiChannel)

    if currentStep.noteLayers[currentStep.selectedLayer[0]].note != 0:
      # Checks whether it should display the values or write - (in case of disabled note)
      octaveString = self.convertDecimalToByteString(currentStep.noteLayers[currentStep.selectedLayer[0]].octave)

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

    return noteString + layerString + octaveString + channelString

  def generatePlayStatusData(self, playing: bool, patternMode: str, saveIndex: int) -> str:
    """ Create Play Status output - playing/pausing + pattern loop LEDs, and save counter """
    gcOutputString = ""
    gcOutput = list("0000")

    # Green LED ON, red OFF if playing, inverted otherwise
    if playing:
      gcOutput[1] = '1'
      gcOutput[2] = '0'
    else:
      gcOutput[1] = '0'
      gcOutput[2] = '1'

    # Yellow LED on if patternMode == single
    if patternMode == 'single':
      gcOutput[3] = '1'

    # Add 4 bits for SaveIndex
    gcOutputString = "".join(gcOutput) + self.binarySaveCounter(saveIndex)

    return gcOutputString

  def generateSetData(self, setIndex: int, setChange: int, setPending: int, setRepeat: bool ) -> str:
    """ Create Set output - set counter and loop status LED """

    setString = setIndex if setChange == 0 else setPending

    setString = self.convertDecimalToByteString(setString)

    # Should we blink?
    if setChange != 0:
      setString = self.blink.blink(setString, True)

    setString = '1' + setString[:-1] if setRepeat else '0' + setString[:-1]

    return setString

  def convertDecimalToByteString(self, decimal: int) -> str:
    """ Convert decimal to 7-segment display output data """

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


  def convertDecimalToNote(self, decimal: int) -> str:
    """ Converts note number to 7-segment display note representation """

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

  def binarySaveCounter(self, index: int) -> str:
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


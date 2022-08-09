import Sequencing.Sequencer as Sequencer

class OutputInterface:
  def __init__(self, hardwareEnabled: bool, shutdownString: str):
    self.hardwareEnabled = False

    if hardwareEnabled:
      import Hardware.HardwareInterface as HWi
      self.sr = HWi.ShiftRegister(21, 20, 16)
      self.hardwareEnabled = True

    self.shutdownString = shutdownString

  def outputData(self, outputData: str) -> None:
    if self.hardwareEnabled:
      self.sr.outputBits(outputData)

  def outputShutdown(self) -> None:
    if self.hardwareEnabled:
      self.sr.outputBits(self.shutdownString)

  def generateByteString(self, sequencer: Sequencer.Sequencer):

    return ""

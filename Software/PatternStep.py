# Pattern Step Class
# 
# Holds pattern's associated step data.
# Sequencer has x patterns (up to 100)
# Each Pattern has 16 PatternSteps
# 
# By Niisse (2021-07-14)
#
# TODO: Rename to Step?

class PatternStep():

  def __init__(self):
    self.enabled = True
    self.note = 0
    self.octave = 0
    self.midiChannel = 0
    self.layer = 0
    self.sustain = False
    self.arm = True

  def disableStep(self):
    # Disables step

    if self.enabled:
      self.enabled = False

  def enableStep(self):
    # Enable step

    if not self.enabled:
      self.enabled = True

  def toggleStep(self):
    # Toggles enable/disable

    if self.enabled:
      self.enabled = False
    else:
      self.enabled = True

  def getState(self):
    # Gets state of enabled
    
    return self.enabled

  def noteUp(self):
    # Increments current note
    # TODO: add check for notelayer

    if self.note < 12:
      self.note += 1
    else: 
      self.note = 0

  def noteDown(self):
    # Decrements current note
    # TODO: add check for notelayer

    if self.note > 0:
      self.note -= 1
    else:
      self.note = 12
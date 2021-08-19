class NoteLayer:
  """Note Layer, holds all necessary note information. 
  
  Allows each step to play multiple notes. There are 10 noteLayers for each step. 
  Sequencer > Pattern > Step > NoteLayer"""

  def __init__(self):
    self.note = 0
    self.octave = 3
    self.midiChannel = 0
    self.sustain = False
    self.arm = True
    self.lastPlayed = (0, 0)      # Used for sustain logic [0] note, [1] channel.

  def setLastPlayed(self, data: tuple):
    """Set last played note"""
    
    self.lastPlayed = data

  def noteUp(self):
    """Increments current note"""

    if self.note < 12:
      self.note += 1
    else: 
      self.note = 0

  def noteDown(self):
    """ Decrements current note"""

    if self.note > 0:
      self.note -= 1
    else:
      self.note = 12

  def octaveUp(self):
    """Increase current octave"""

    if self.octave < 9:
      self.octave += 1
    else:
      self.octave = 0

  def octaveDown(self):
    """Decrease current octave"""
    
    if self.octave > 0:
      self.octave -= 1
    else:
      self.octave = 9
  
  def channelUp(self):
    """ Increment current midi channel. Sets last used channel if midiChannel == 0"""

    if self.midiChannel < 9:
      self.midiChannel += 1
    else:
      self.midiChannel = 0

  def channelDown(self):
    """Increment current midi channel"""

    if self.midiChannel > 0:
      self.midiChannel -= 1
    else:
      self.midiChannel = 9

  def toggleSustain(self):
    """ Toggles sustain on/off"""
    
    self.sustain = False if self.sustain else True
  
  def toggleArm(self):
    """ Toggles arm on/off; disabled arm will show notes but not play them"""
    
    self.arm = False if self.arm else True
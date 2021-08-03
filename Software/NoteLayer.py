# Note Layer class

class NoteLayer:
  def __init__(self):
    self.note = 0
    self.octave = 0
    self.midiChannel = 0
    self.layer = 0
    self.sustain = False
    self.arm = True

  def noteUp(self):
    # Increments current note

    if self.note < 12:
      self.note += 1
    else: 
      self.note = 0

  def noteDown(self):
    # Decrements current note

    if self.note > 0:
      self.note -= 1
    else:
      self.note = 12

  def octaveUp(self):
    # Increase current octave

    if self.octave < 9:
      self.octave += 1
    else:
      self.octave = 0

  def octaveDown(self):
    # Decrease current octave
    
    if self.octave > 0:
      self.octave -= 1
    else:
      self.octave = 9
  
  def channelUp(self):
    # Increment current midi channel

    if self.midiChannel < 9:
      self.midiChannel += 1
    else:
      self.midiChannel = 0
    

  def toggleSustain(self):
    # Toggles sustain on/off
    
    self.sustain = False if self.sustain else True
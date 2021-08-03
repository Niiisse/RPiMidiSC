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
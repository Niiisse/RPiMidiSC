class GlobalVars:
  # All of these vars are loaded from config on initialize
  def __init__(self):
    self.seqstep = 0         # Sequencer step
    self.bpm = 0             # Tempo
    self.playing = True      # Playing / paused status
    self.patternStep = 0     # Current pattern no.
    self.patternChange = 0   # signals pattern change for next measure
    self.patternPending = 0  # Used in changing pattern


  # TODO: are these really necessary?
  def setSeqstep(self, seqstep):
    GlobalVars.seqstep = seqstep

  def setBPM(self, bpm):
    GlobalVars.bpm = bpm

  def setPatternStep(self, patternStep):
    GlobalVars.patternStep = patternStep
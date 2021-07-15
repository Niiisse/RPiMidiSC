class GlobalVars:
  # All of these vars are loaded from config on initialize
  
  #seqstep = 0         # Sequencer step
  #bpm = 0             # Tempo
  #playing = True      # Playing / paused status
  #patternStep = 0     # Current pattern no.
  # patternChange = 0   # signals pattern change for next measure
  # patternPending = 0  # Used in changing pattern
  # patternEditing = False


  # TODO: are these really necessary?
  def setSeqstep(self, seqstep):
    GlobalVars.seqstep = seqstep

  def setBPM(self, bpm):
    GlobalVars.bpm = bpm

  def setPatternStep(self, patternStep):
    GlobalVars.patternStep = patternStep
class GlobalVars:
  # All of these vars are loaded from config on initialize

  seqstep = 0         # Sequencer step
  bpm = 0             # Tempo
  playing = True      # Playing / paused status
  patternStep = 0     # Current pattern no.
  patternChange = 0   # signals pattern change for next measure
  patternPending = 0  # Used in changing pattern


  # TODO: are these really necessary?
  def setSeqstep(self, seqstep):
    GlobalVars.seqstep = seqstep

  def getSeqstep(self):
    return GlobalVars.seqstep

  def setBPM(self, bpm):
    GlobalVars.bpm = bpm
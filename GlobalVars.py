class GlobalVars:
  # All of these vars are loaded from config on initialize

  seqstep = 0         # Sequencer step
  bpm = 0             # Tempo
  playing = True      # Playing / paused status
  patternStep = 1         # Current pattern no.


  # TODO: are these really necessary?
  def setSeqstep(self, seqstep):
    GlobalVars.seqstep = seqstep

  def getSeqstep(self):
    return GlobalVars.seqstep
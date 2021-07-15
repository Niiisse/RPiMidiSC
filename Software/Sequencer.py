from . import Pattern

class Sequencer:

  def __init__(self, patternAmount, sequencerSteps, bpm, seqstepmax, seqstepsize):
    # Get amount of patterns, init patterns list with x empty patterns

    # Sequencer vars
    self.playing = True
    self.seqstep = 0
    self.seqstepmax = seqstepmax
    self.seqstepsize = seqstepsize
    self.sequencerSteps = sequencerSteps
    self.bpm = bpm
    self.start_timer = True

    # Pattern Variables
    self.patternAmount = patternAmount                                          # Amount of patterns
    self.patterns = [Pattern.Pattern(sequencerSteps) for i in range(patternAmount)]   # Array that holds Patterns
    self.patternStep = 1                                                        # Current pattern
    self.patternChange = 0                                                      # Signals pattern change for next measure
    self.patternPending = 0                                                     # Used in changing pattern
    self.patternEditing = False                                                 # Currently in editing mode?

  # TODO: Move timer in here. Add function tick. Move pattern stepping etc to here.
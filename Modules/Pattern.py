from . import PatternStep

  # Pattern Class
  # 
  # Holds an array of PatternSteps associated with this pattern 

class Pattern:
  def __init__(self, sequencerSteps):
    self.steps = sequencerSteps
    self.patternSteps = [PatternStep.PatternStep() for i in range(self.steps)]
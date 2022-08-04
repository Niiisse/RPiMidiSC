from . import Step

  # Pattern Class
  # 
  # Holds an array of PatternSteps associated with this pattern 

class Pattern:
  def __init__(self, sequencerSteps):
    self.stepsAmount = sequencerSteps
    self.steps = [Step.Step() for i in range(self.stepsAmount)]

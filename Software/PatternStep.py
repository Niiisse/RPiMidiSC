# Pattern Step Class
# 
# Holds sequencer/pattern's associated step data.
# Sequencer has x patterns (up to 100)
# Each Pattern has 16 PatternSteps
# 
# By Niisse (2021-07-14)

class PatternStep():

  def __init__(self):
    self.enabled = True

  def disableStep(self):
    # Disables step

    if self.enabled:
      self.enabled = False

  def enableStep(self):
    # Enable step

    if not self.enabled:
      self.enabled = True

  def getState(self):
    # Gets state of enabled
    return self.enabled
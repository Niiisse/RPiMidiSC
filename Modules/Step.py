from . import NoteLayer

# Pattern Step Class
# 
# Holds pattern's associated step data.
# Sequencer has x patterns (up to 100)
# Each Pattern has 16 PatternSteps
# Each patternStep has 9 noteLayers which
# contain the actual data
# 
# By Niisse (2021-07-14)
#
# TODO: Rename to Step?

class Step():

  def __init__(self):
    self.enabled = True
    self.noteLayerAmount = 10
    self.noteLayers = [NoteLayer.NoteLayer() for i in range(self.noteLayerAmount)]
    self.selectedLayer = [0, 1, 2, 3]

  def disableStep(self):
    # Disables step

    if self.enabled:
      self.enabled = False

  def enableStep(self):
    # Enable step

    if not self.enabled:
      self.enabled = True

  def toggleStep(self):
    # Toggles enable/disable

    if self.enabled:
      self.enabled = False
    else:
      self.enabled = True

  def getState(self):
    # Gets state of enabled
    
    return self.enabled

  def layerUp(self):
    # Changes note layer. TODO: multiple NCM support goes here, eventually
    
    if self.selectedLayer[0] < 9:
      self.selectedLayer[0] += 1
    else:
      self.selectedLayer[0] = 0
      
  def layerDown(self):
    # Changes note layer. TODO: multiple NCM support goes here, eventually

    if self.selectedLayer[0] > 0:
      self.selectedLayer[0] -= 1
    else:
      self.selectedLayer[0] = 9

  def checkOtherLayers(self):
    # Looks thru other layers and sees if a note is active, if so, show LED
    output = False

    for x in range(10):                                                                     # Loop over all layers
      if x != self.selectedLayer[0]:                                                        # Exclude self
        if self.noteLayers[x].note != 0 or self.noteLayers[x].sustain:            # No other notes and sustain is off?
          output = True 

    return output

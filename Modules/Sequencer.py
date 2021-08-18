import time
from . import Pattern, SaveLoad

class Sequencer:
  """ Handles all sequencer-related functions & midi output """

  def __init__(self, patternAmount: int, sequencerSteps: int, bpm: int, seqstepsize: int, midiEnabled: bool, previewNoteDuration: int):

    # Sequencer Variables
    self.playing = True                               # Whether the sequencer is currently playing or paused 
    self.seqstep = 0                                  # Current step within pattern         
    self.stepSize = seqstepsize                       # Amount to increment with per step. TODO: see if this can go
    self.sequencerSteps = sequencerSteps              # Total amout of steps per pattern
    self.bpm = bpm                                    # Current tempo
    self.previewNotesOff = []                         # List that holds notes that are to be turned off
    self.previewNoteDuration = previewNoteDuration  # How long preview nots should play
    
    # Timer Variables
    self.timerShouldTick = True                   # Make sequencer go brrr
    self.tic = time.perf_counter()                # Sets timestamp to compare against

    # Pattern Variables
    self.patternAmount = patternAmount                                                # Amount of patterns
    self.patterns = [Pattern.Pattern(sequencerSteps) for i in range(patternAmount+1)] # List that holds Patterns
    self.patternStep = 1                                                              # Current pattern
    self.patternChange = 0                                                            # Signals pattern change for next measure
    self.pendingPattern = 0                                                           # Used in changing pattern
    self.patternEditing = False                                                       # Currently in editing mode?
    self.patternMode = "auto"                                                         # Auto loops patterns, single loops 1

    # Misc
    self.noteLayerAmount = 10         # Added this for not having to hardcode noteLayer amount when saving/loading, i think
    self.midiEnabled = midiEnabled    # Whether or not to enable MIDI output
    
    if midiEnabled:
      from . import Midi
      self.midiInterface = Midi.MidiInterface()

    # Saving / Loading
    self.saveLoad = SaveLoad.SaveLoad()

  def play(self):
    # Plays. (i don't know what you expected, tbh)

    if not self.playing: self.playing = True

  def pause(self):
    # You won't believe it. Pauses sequencer.
    
    if self.playing: self.playing = False

  def save(self):
    """ TODO: all the things """

    self.saveLoad.save(0, self)
    pass

  def load(self):
    """ TODO: all the things """

    self.saveLoad.load(0, self)

  def togglePlay(self):
    # Prepare to be amazed. Toggles pause/play

    if self.playing: self.playing = False
    else:
      self.playing = True
      #self.seqstep -= 1
      self.sequencerStep
      #self.sendMidi()       # Call this so the first step starts playing when unpausing

  def tickTimer(self):
    # 'Ticks' timer; sets new timestamp for comparison

    self.tic = time.perf_counter()

  def timer(self):
    # Handles sequencer's timer, responsible for stepping
    # First check makes sure we're playing and not editing a pattern
    # Second makes sure we don't infinitely tick the timer
    
    if self.playing and not self.patternEditing:
      if self.timerShouldTick:
        self.timerShouldTick = False
        self.tickTimer()

      # Has enough time gone by for us to tick?
      # " if current time - last tic time > bpm time" ...
      # 60 / bpm for changing bpm to bps; / 4 for sequencer spacing purposes)
      
      if time.perf_counter() - self.tic > (60 / self.bpm / 4):
        self.sequencerStep()
        self.timerShouldTick = True

  def toggleEditMode(self):
    # Toggles Pattern Editing on or off. So glad I write these descriptive comments

    self.patternEditing = False if self.patternEditing else True

  def changePendingPattern(self):
    # Changes pattern to pending pattern
    
    self.patternStep = self.pendingPattern
    self.patternChange = 0
    self.pendingPattern = 0

  def changePattern(self, changeValue):
    # Instantly changes pattern. Useful in editing mode. changeValue needs an int
    
    self.patternStep += changeValue
    # TODO: clamping?

  def togglePatternMode(self):
    """ Toggles pattern mode between auto or single """

    self.patternMode = "auto" if self.patternMode == "single" else "single"

  def sequencerStep(self):
    # Executes each step
    self.sendMidi(False) # Midi Output

    # Checks if we should increase seqstep or roll back
    if self.seqstep < self.sequencerSteps - 1:
      self.seqstep += self.stepSize
    else:
      self.finalStepInPattern()

  def finalStepInPattern(self):
    """ Executed at the final step in a pattern
    
    Decides if pattern will be changed, depending on patternMode. """

    # Clamp step; roll back when too high and process pattern stuff
    self.seqstep = 0

    # Apply pending pattern if applicable...
    if self.patternChange != 0:
      self.changePendingPattern()

    # Else, increment pattern by 1 if mode = auto
    elif self.patternMode == "auto":
      if self.patternStep < self.patternAmount:
        self.patternStep += 1
      else:
        self.patternStep = 1
    
    # # Stepping backwards?
    # elif self.seqstep < 0:
    #   self.seqstep = self.sequencerSteps
    #   self.patternStep -= 1

  def sendMidi(self, previewNote: bool):
    """ Collects all notes that should get played.

    previewNote = only changed note (for previewing inputs)
    previewNote off sends all notes in current layer (normal behaviour) """

    if self.midiEnabled:
      
      midiData = []     # List of noteLayer objects

      # If preview, send only current activelayer
      if previewNote:
        x = self.patterns[self.patternStep].patternSteps[self.seqstep]
        midiData.append(x.noteLayers[x.selectedLayer[0]])
        addPreviewNoteOff(x.noteLayers[x.selectedLayer[0]])
      
      else:
      # Check all noteLayers in current step, if that step is enabled; send their data, if relevant, to midi processing
        if self.patterns[self.patternStep].patternSteps[self.seqstep].enabled:
          for noteLayer in self.patterns[self.patternStep].patternSteps[self.seqstep].noteLayers:
            midiData.append(noteLayer)
            noteLayer.lastPlayed = (noteLayer.note, noteLayer.midiChannel)

      self.midiInterface.playNote(midiData)
    
    def addPreviewNoteOff(self, midiData):
      """ Add notes to a temp list that will send noteOff for preview notes """
      data = (midiData, time.time())
      self.previewNotesOff.append(data)
      
    def checkPreviewNotesOff(self):
      """ Check if any previewNotes are ready to be turned off, to prevent them from playing indefinitely """

      if len(self.previewNotesOff) > 0:
        toc = time.time()
        
        for note in self.previewNotesOff:
          if note[1] - toc > self.previewNoteDuration:
            self.midiInterface
            pass
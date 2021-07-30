import time
from . import Pattern, Clamp
import random

# Sequencer 
#
# Handles most, if not all, of the music-related functions.
# TODO: seqstep, pending clamping 
# 
# By Niisse


class Sequencer:

  clamp = Clamp.clamp

  def __init__(self, patternAmount, sequencerSteps, bpm, seqstepsize):

    # Sequencer Variables
    self.playing = True                           # Whether the sequencer is currently playing or paused 
    self.seqstep = 0                              # Current step within pattern         
    self.stepSize = seqstepsize                   # Amount to increment with per step. TODO: see if this can go
    self.sequencerSteps = sequencerSteps          # Total amout of steps per pattern
    self.bpm = bpm                                # Current tempo
    
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

    random.seed()

  def randomiseData(self):
    # Randomises note data for testing

    for i in range(self.patternAmount+1):
      for o in range(self.sequencerSteps):
        self.patterns[i].patternSteps[o].note = random.randint(0, 12)
        self.patterns[i].patternSteps[o].layer = random.randint(0, 3)
        self.patterns[i].patternSteps[o].octave = random.randint(0, 9)
        self.patterns[i].patternSteps[o].midiChannel = random.randint(0, 9)

  def play(self):
    # Plays. (i don't know what you expected, tbh)

    if not self.playing: self.playing = True

  def pause(self):
    # You won't believe it. Pauses sequencer.
    
    if self.playing: self.playing = False

  def togglePlay(self):
    # Prepare to be amazed. Toggles pause/play

    self.playing = False if self.playing else True

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
        self.seqstep += self.stepSize
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

  def stepSequencer(self):
    # Steps the sequencer. Handles pattern changing and such as well

    # Clamp step; roll back when too high and process pattern stuff
    if self.seqstep > self.sequencerSteps - self.stepSize:
      self.seqstep = 0

      # Apply pending pattern if applicable...
      if self.patternChange != 0:
        self.changePendingPattern()

      # Else, increment pattern by 1
      else:
        self.patternStep += 1
    
    # Stepping backwards?
    elif self.seqstep < 0:
      self.seqstep = self.sequencerSteps
      self.patternStep -= 1
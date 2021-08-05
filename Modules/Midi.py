# MIDI Interface

import pygame.midi
#import time

class MidiInterface:

  def __init__(self):
    pygame.midi.init()                    # Init pygame midi library

    self.velocity = 100

    # TODO: Figure out way to select midi device

    self.interface = pygame.midi.Output(2)
    self.interface.set_instrument(0, 0)      # instrument id, channel #TODO: use set instrument for midi channel change
    
    # For checking whether notes should be disabled
    self.pastNotes = []

    # For keeping track of what notes are currently on
    self.noteOnList = []

    # Dict that holds my note structure (1-12) and converts it to midi note
    self.noteToMidi = {
      1: 12,      # C
      2: 13,      # C#
      3: 14,      # D
      4: 15,      # D#
      5: 16,      # E
      6: 17,      # F
      7: 18,      # F#
      8: 19,      # G
      9: 20,      # G#
      10: 21,     # A
      11: 22,     # A#
      12: 23,     # B
    }

  def calculateNoteValue(self, note, octave):
    # My notes to MIDI notes
    # If note == 0 && sustain = 1, don't cut note
    # if note == 0 && sustain = 0, note off
    # Each octave gives +12
    # output

    # No disabled note
    if note != 0:
      outputNote = self.noteToMidi[note] + (octave*12)
      return outputNote

    pass

  def playNote(self, midiData):
    # TODO: figure out how to decide if currently playing notes should be stopped
    #       output.write for multiple
    
    ## DISABLING OLD NOTES ##
    # Compare current note. If channel matches and note = 0 (will always be sustain cus of sequencer code)
    # don't turn it off. If no match was found on channel and no new note is played, turn off.
    #
    # [i for i in range(len(a)) if a[i] > 2]
    #  > [2, 5]

    toRemove = []         # Will hold indexes of items that should be removed from pastNotes
    for idx, playedNote in enumerate(self.pastNotes):

      # [0] = played note; [1] = channel
      self.interface.note_off(playedNote[0], 0, playedNote[1])    # Stop playing note
      toRemove.append(idx)                                        # Add idx to removelist

    for item in toRemove:                                       # Loop over to-be-removed items
      try: del self.pastNotes[item]                                    # YEEEET
      except: pass
      
    toRemove.clear()                                            # Clear list
      

    ## PLAYING NEW NOTES ##
    
    # Loop over received midiData
    for noteLayer in midiData: 
      
      # New note
      if noteLayer.note != 0:
        
        outputNote = self.calculateNoteValue(noteLayer.note, noteLayer.octave)
        self.interface.note_on(outputNote, self.velocity, noteLayer.midiChannel)
        
        playedNote = [outputNote, noteLayer.midiChannel]
        self.pastNotes.append(playedNote)

    #self.pastNotes.append(outputNote)
    
    #self.player.note_off(outputNote)

    #self.interface.note_on(outputNote, 100)

  def cleanUp(self):
    pygame.midi.quit()
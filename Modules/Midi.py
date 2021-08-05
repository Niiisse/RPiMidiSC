# MIDI interface

import rtmidi, time

class Midi:
  def __init__(self):
    # rtmidi setup
    
    self.midiOut = rtmidi.MidiOut()
    self.availablePorts = self.midiOut.get_ports()
    
    # Setup first available midi device if possible
    if self.availablePorts:
      self.midiOut.open_port(0)
    else:
      self.midiOut.open_virtual_port("RPiMIDISC Virtual Out")

  def playNoteTest(self):
    with self.midiOut:
      note_on = [0x90, 60, 112] # channel 1, middle C, velocity 112
      note_off = [0x80, 60, 0]
      self.midiOut.send_message(note_on)
      time.sleep(0.5)
      self.midiOut.send_message(note_off)
      time.sleep(0.1)

  #del midiOut



  
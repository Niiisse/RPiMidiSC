# MIDI Interface

import pygame.midi
#import time

class MidiInterface:

  def __init__(self):
    pygame.midi.init()

    #print(pygame.midi.get_default_output_id())
    #print(pygame.midi.get_device_info(2))
    # TODO: Figure out way to select midi device

    self.player = pygame.midi.Output(2)

    self.player.set_instrument(0)

    # print('Playing...')

  def playNote(self):
    self.player.note_off(64)

    self.player.note_on(64, 100)

  def cleanUp(self):
    pygame.midi.quit()
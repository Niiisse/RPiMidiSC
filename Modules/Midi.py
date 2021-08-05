# MIDI Interface

import pygame.midi
#import time

class MidiInterface:

  def __init__(self):
    pygame.midi.init()

    #print(pygame.midi.get_default_output_id())
    #print(pygame.midi.get_device_info(2))

    player = pygame.midi.Output(0)

    player.set_instrument(0)

    print('Playing...')

player.note_on(64, 100)
time.sleep(1)
player.note_off(64)

print('Played')

pygame.midi.quit()
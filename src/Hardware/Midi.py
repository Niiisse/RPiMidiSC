# MIDI Interface

import pygame.midi


class MidiInterface:

    def __init__(self):
        pygame.midi.init()  # Init pygame midi library
        self.toRemove = []

        self.velocity = 100

        # TODO: Figure out way to select midi device

        self.interface = pygame.midi.Output(2)
        self.interface.set_instrument(0, 0)

        # For keeping track of what notes are currently on
        self.noteOnList = []

        # Dict that holds my note structure (1-12) and converts it to midi note
        self.noteToMidi = {
            1: 12,  # C
            2: 13,  # C#
            3: 14,  # D
            4: 15,  # D#
            5: 16,  # E
            6: 17,  # F
            7: 18,  # F#
            8: 19,  # G
            9: 20,  # G#
            10: 21,  # A
            11: 22,  # A#
            12: 23,  # B
        }

    def calculateNoteValue(self, note, octave):
        # My notes to MIDI notes
        # If note == 0 && sustain = 1, don't cut note
        # if note == 0 && sustain = 0, note off
        # Each octave gives +12
        # output

        # No disabled note
        if note != 0:
            outputNote = self.noteToMidi[note] + ((octave - 1) * 12)
            return outputNote

        pass

    def playNote(self, noteLayers):
        # midiData holds 10 noteLayers

        # TODO: output.write for multiple

        # pastNotes is a list of notes that are still playing. If there's a new note that matches
        # an entry (criteria: no new note on channel but sustain is enabled), don't delete it and check next time

        # DELETE OLD NOTES?
        for idx, playedNote in enumerate(self.noteOnList):  # playedNote[0] = note; [1] = channel, [2] = noteLayer

            try:  # FIXME: figure out why this occasionally crashes
                if noteLayers[playedNote[2]].sustain == False:
                    self.interface.note_off(playedNote[0], 0, playedNote[1])  # Stop playing note
                    self.toRemove.append(playedNote)  # Add idx to removelist

            except:
                pass

        for item in self.toRemove:  # Loop over to-be-removed items
            idx = self.noteOnList.index(item)
            del self.noteOnList[idx]  # YEEEET

        self.toRemove.clear()

        # Loop over received midiData
        for idx, noteLayer in enumerate(noteLayers):
            if noteLayer.note != 0 and noteLayer.arm == True:
                outputNote = self.calculateNoteValue(noteLayer.note, noteLayer.octave)  # Calculate note value; store it
                self.interface.note_on(outputNote, self.velocity, noteLayer.midiChannel)  # Play it
                print("OUTPUT note {}, octave {}, channel {}, vel {}, mod {}, on layer {}".
                      format(outputNote, noteLayer.octave, noteLayer.midiChannel, noteLayer.velocity,
                             noteLayer.modulation, idx))

                playedNote = [outputNote, noteLayer.midiChannel, idx]  # Save as playedNote
                self.noteOnList.append(playedNote)  # Add to list of played notes

    def allNotesOff(self):
        """ MIDI Panic. Turns off all notes, empties noteOnList """

        for note in self.noteOnList:
            self.interface.note_off(note[0], 0, note[1])

        self.noteOnList.clear()

    def cleanUp(self):
        pygame.midi.quit()

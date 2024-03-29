import time, config
from . import SaveLoad, Set


class Sequencer:
    """ Handles all sequencer-related functions & midi output """

    def __init__(self):

        # Sequencer Variables
        self.playing = False                            # Whether the sequencer is currently playing or paused
        self.seqstep = 0                                # Current step within pattern
        self.stepSize = config.sequencer['seqstepsize']   # Amount to increment with per step. TODO: see if this can go
        self.sequencerSteps = config.sequencer['seqstepmax']            # Total amout of steps per pattern
        self.previewNotesOff = []                       # List that holds notes that are to be turned off
        self.previewNoteDuration = config.sequencer['previewNoteDuration'] # How long preview notes should play
        self.lastUsedMidiChannel = 0                    # Last-entered MIDI channel
        self.lastUsedLayer = 0                          # Last-entered layer
        self.lastUsedOctave = 3                         # Last-entered octave

        # Timer Variables
        self.timerShouldTick = True                     # Make sequencer go brrr
        self.tic = time.perf_counter()                  # Sets timestamp to compare against

        # Pattern Variables
        self.patternAmount = config.pattern['patternAmount']              # Amount of patterns
        self.patternIndex = 1                           # Current pattern
        self.patternChange = 0                          # Signals pattern change for next measure
        self.pendingPattern = 0                         # Used in changing pattern
        self.patternMode = "auto"                       # Auto loops patterns, single loops 1

        # Sets
        self.setsAmount = 15
        self.setIndex = 0                               # Currently active set
        self.sets = [Set.Set(self.sequencerSteps, self.patternAmount) for i in range(self.setsAmount + 1)]
        self.setRepeat = False                          # Whether sets loop or not
        self.setChange = 0                              # For changing
        self.setPending = 0

        # Misc
        self.noteLayerAmount = 10       # Added this for not having to hardcode noteLayer amount when saving/loading, i think
        self.savesTotal = 15            # Total number of saves
        self.prepareReset = False       # Reset flag
        self.canReset = True

        self.midiEnabled = False
        self.hardwareEnabled = config.general['hardware_enabled']

        if config.general['midiEnabled']:
            from Hardware import Midi
            self.midiInterface = Midi.MidiInterface()
            self.midiEnabled = True

        # Saving / Loading
        self.saveLoad = SaveLoad.SaveLoad()

        # When initialised, check what save was last loaded, and reopen it
        self.saveIndex = self.saveLoad.readLastLoadedSaveIndex()  # set index of loaded savefile
        self.load(self.saveIndex)

    def clearSequencer(self):
        """ Resets sequencer """
        print("clearing")

        self.canReset = False
        self.prepareReset = False
        self.playing = False
        self.seqstep = 0
        self.setIndex = 0
        self.patternIndex = 1
        self.initSets()

    def play(self):
        # Plays. (i don't know what you expected, tbh)

        if not self.playing: self.playing = True

    def pause(self):
        # You won't believe it. Pauses sequencer.

        if self.playing: self.playing = False

        if self.midiEnabled:
            self.midiInterface.allNotesOff()

    def initSets(self):
        """ Re-initializes pattern list to deal with differing saves """

        self.sets = [Set.Set(self.sequencerSteps, self.patternAmount) for i in range(self.setsAmount + 1)]

    def togglePlay(self):
        # Prepare to be amazed. Toggles pause/play

        if self.playing:
            self.playing = False

            if self.midiEnabled:
                self.midiInterface.allNotesOff()
        else:
            self.playing = True
            # self.seqstep -= 1
            self.sequencerStep
        # self.sendMidi()       # Call this so the first step starts playing when unpausing

        # Disables canReset lockout if applicable
        if self.canReset == False:
            self.canReset = True

    def tickTimer(self):
        # 'Ticks' timer; sets new timestamp for comparison

        self.tic = time.perf_counter()

    def update(self) -> None:
        """ Handles sequencer's timer
        Responsible for stepping, makes sure we don't infinitely tick the timer """

        if self.playing:
            if self.timerShouldTick:
                self.timerShouldTick = False
                self.tickTimer()

            # Has enough time gone by for us to tick?
            # " if current time - last tic time > bpm time" ...
            # 60 / bpm for changing bpm to bps; / 4 for sequencer spacing purposes)

            if time.perf_counter() - self.tic > (60 / self.sets[self.setIndex].bpm / 4):
                self.sequencerStep()
                self.timerShouldTick = True

    def noteDown(self):
        """ Change note down event

        If note == 0 (off), set selectedLayer, octave and midiChannel to last-used values """

        currentStep = self.sets[self.setIndex].patterns[self.patternIndex].steps[self.seqstep]

        if currentStep.noteLayers[currentStep.selectedLayer[0]].note == 0:
            currentStep.selectedLayer[0] = self.lastUsedLayer
            currentStep.noteLayers[currentStep.selectedLayer[0]].midiChannel = self.lastUsedMidiChannel
            currentStep.noteLayers[currentStep.selectedLayer[0]].octave = self.lastUsedOctave

        currentStep.noteLayers[currentStep.selectedLayer[0]].noteDown()

        self.sendMidi(True)


    def noteUp(self):
        """ Change note up event

        If note == 0 (off), set selectedLayer, octave and midiChannel to last-used values
        TODO: multiple NCM support """

        currentStep = self.sets[self.setIndex].patterns[self.patternIndex].steps[self.seqstep]

        if currentStep.noteLayers[currentStep.selectedLayer[0]].note == 0:
            currentStep.selectedLayer[0] = self.lastUsedLayer
            currentStep.noteLayers[currentStep.selectedLayer[0]].midiChannel = self.lastUsedMidiChannel
            currentStep.noteLayers[currentStep.selectedLayer[0]].octave = self.lastUsedOctave

        currentStep.noteLayers[currentStep.selectedLayer[0]].noteUp()

        self.sendMidi(True)

    def changePendingPattern(self):
        """ Changes pattern to pending pattern """

        self.patternIndex = self.pendingPattern
        self.patternChange = 0
        self.pendingPattern = 0

    def changePendingSet(self):
        """ Changes set to pending set """

        self.setIndex = self.setPending
        self.setChange = 0
        self.setPending = 0

        self.patternChange = 0
        self.pendingPattern = 0
        self.patternIndex = 1

    def patternUp(self):
        """ Instantly change pattern, used when sequencer is paused. Also moves step back to 0. """
        if self.patternIndex == self.patternAmount:
            self.patternIndex = 1
        else:
            self.patternIndex += 1

        self.seqstep = 0

    def patternDown(self):
        """ Instantly change pattern, used when sequencer is paused. Also moves step back to 0. """

        if self.patternIndex == 1:
            self.patternIndex = self.patternAmount
        else:
            self.patternIndex -= 1

        self.seqstep = 0

    def setUp(self):
        """ Go up 1 set """

        if self.setIndex == self.setsAmount:
            self.setIndex = 0
        else:
            self.setIndex += 1

        self.patternIndex = 1
        self.seqstep = 0

    def setDown(self):
        """ Go down 1 set """

        if self.setIndex == 0:
            self.setIndex = self.setsAmount
        else:
            self.setIndex -= 1

        self.patternIndex = 1
        self.seqstep = 0

    def toggleSetRepeat(self):
        """ Toggles set repeat (wow) """

        self.setRepeat = False if self.setRepeat == True else True

    def changeSave(self, oldSaveIndex: int):
        """ Changes save slot. Saves current save, then loads new save """

        # self.saveLoad.save(oldSaveIndex, self)
        # self.saveLoad.load(self.saveIndex, self)
        self.load(self.saveIndex)

    def changePattern(self, changeValue):
        # Instantly changes pattern. Useful in editing mode. changeValue needs an int

        self.patternIndex += changeValue

    # TODO: clamping?

    def clampPendingSetStepping(self):
        """ Calculate pending set stepping """

        if self.setChange != 0:
            if self.setChange > self.setsAmount - self.setIndex:
                self.setChange -= self.setsAmount + 1

            if self.setChange + self.setIndex < 0:
                self.setChange += self.setsAmount + 1

        self.setPending = self.setIndex + self.setChange

    def togglePatternMode(self):
        """ Toggles pattern mode between auto or single """

        self.patternMode = "auto" if self.patternMode == "single" else "single"

    def sequencerStep(self):
        # Executes each step

        if self.midiEnabled:
            self.sendMidi(False)  # Midi Output

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

        if self.setChange != 0:
            self.changePendingSet()

        # Apply pending pattern if applicable...
        elif self.patternChange != 0:
            self.changePendingPattern()

        # Else, increment pattern by 1 if mode = auto
        elif self.patternMode == "auto":
            if self.patternIndex < self.patternAmount:
                self.patternIndex += 1

            else:
                # Pattern rolling over means end of current Set
                self.patternIndex = 1

                # Set switching
                if self.setRepeat == False:
                    self.setUp()

    # # Stepping backwards?
    # elif self.seqstep < 0:
    #   self.seqstep = self.sequencerSteps
    #   self.patternIndex -= 1

    def sendMidi(self, previewNote: bool):
        """ Collects all notes that should get played.

        previewNote = only changed note (for previewing inputs)
        previewNote off sends all notes in current layer (normal behaviour) """


        midiData = []  # List of noteLayer objects

        # If preview, send only current activelayer
        if previewNote:
            x = self.sets[self.setIndex].patterns[self.patternIndex].steps[self.seqstep]
            midiData.append(x.noteLayers[x.selectedLayer[0]])
        # self.addPreviewNoteOff(x.noteLayers[x.selectedLayer[0]])

        else:
            # Check all noteLayers in current step, if that step is enabled; send their data, if relevant, to midi processing
            if self.sets[self.setIndex].patterns[self.patternIndex].steps[self.seqstep].enabled:
                for noteLayer in self.sets[self.setIndex].patterns[self.patternIndex].steps[
                        self.seqstep].noteLayers:
                    midiData.append(noteLayer)
                    noteLayer.lastPlayed = (noteLayer.note, noteLayer.midiChannel)

        if self.midiEnabled:
            self.midiInterface.playNote(midiData)

    def reset(self, metaRows: list[dict], index: int) -> None:
        """ Resets sequencer with data from loaded savefile """

        self.playing = False
        self.seqstep = 0
        self.setInde = 0
        self.patternIndex = 1
        self.patternAmount = int(metaRows[index]['patternAmount'])
        self.initSets()
        self.patternMode = metaRows[index]['patternMode']
        self.setRepeat = bool(int((metaRows[index]['setRepeat'])))

    def saveLoadAnim(self):
        outputString = config.misc['hw_off_string']
        outputList = list()

        for i in range(4):
            outputList = list(outputString)

        for bit in range(len(outputList)):
            if outputList[bit] == '0':
                outputList[bit] = '1'
            else:
                outputList[bit] = '0'

            outputString = ""
            outputString = outputString.join(outputList)
            # self.sr.outputBits(outputString)

        time.sleep(0.05)

    # Saving / Loading #

    def save(self, index: int):
        """ Saves Sequencer state into saveslot """

        self.saveLoad.save(index,
                           self.setsAmount+1,
                           self.sets,
                           self.setRepeat,
                           self.patternMode,
                           self.patternAmount,
                           self.noteLayerAmount,
                           self.sequencerSteps,
                           )

    def load(self, index: int):
        """ Loads a CSV file, applies contents to Sequencer.
        Load metadata and a big ol' CSV file containing the song's data, then loop over relevant sequencer sections
        and fill it with the CSV's data. Lastly, save currently loaded save index to lastLoadedSave in data.csv"""

        metaRows = self.saveLoad.readMetadata()
        self.reset(metaRows, index)

        rows = self.saveLoad.readRowData(index)

        # set bpm
        for i in range(self.setsAmount + 1):
            self.sets[i].bpm = int(metaRows[i]['bpm'])

        # Loop over all rows, copy data to sequencer, check prevents index out of bounds
        for idx, row in enumerate(rows):
            if idx < self.setsAmount * self.patternAmount * self.noteLayerAmount * self.sequencerSteps:
                step = self.sets[int(row['set'])].patterns[int(row['pattern'])].steps[int(row['step'])]
                layer = self.sets[int(row['set'])].patterns[int(row['pattern'])].steps[int(row['step'])].noteLayers[int(row['layer'])]

                layer.arm = bool(int(row['arm']))
                layer.midiChannel = int(row['channel'])
                layer.lastPlayed = (int(row['lastPlayedNote']), int(row['lastPlayedChannel']))
                layer.note = int(row['note'])
                layer.octave = int(row['octave'])
                layer.sustain = bool(int(row['sustain']))
                step.selectedLayer=[int(row['selectedLayer0']), int(row['selectedLayer1']), int(row['selectedLayer2']), int(row['selectedLayer3'])]
                step.enabled = bool(int(row['enabled']))

        # save lastloadedindex in load
        self.saveLoad.saveLastLoadedSaveIndex(index)

    def saveUp(self):
        """ Handles saveIndex logic """
        oldSaveIndex = self.saveIndex

        if self.saveIndex == self.savesTotal:
            self.saveIndex = 0
        else:
            self.saveIndex += 1

        self.changeSave(oldSaveIndex)

    def saveDown(self):
        """ Handles saveIndex logic """

        oldSaveIndex = self.saveIndex

        if self.saveIndex == 0:
            self.saveIndex = self.savesTotal
        else:
            self.saveIndex -= 1

        self.changeSave(oldSaveIndex)

    def processInput(self, action: str) -> None:
        """ Handles input """

        # Reset prepareReset if button has been let go
        if action != "prepareReset" and self.prepareReset == True:
            self.prepareReset = False

        if action == "doReset":
            print("didReset")
            self.clearSequencer()

        # BPM up & down; clamping
        elif action == "bpmUp":
            print("btnUp!")
            if self.sets[self.setIndex].bpm < 999:
                self.sets[self.setIndex].bpm += 1
            else:
                self.sets[self.setIndex].bpm = 1

        elif action == "bpmDown":
            if self.sets[self.setIndex].bpm > 1:
                self.sets[self.setIndex].bpm -= 1
            else:
                self.sets[self.setIndex].bpm = 999


        # self.stepping next & previous; clamping
        # FIXME: Move to Sequencer
        # TODO: NCM
        elif action == "seqStepUp":
            self.seqstep += self.stepSize

            if self.seqstep > self.sequencerSteps - self.stepSize:
                self.seqstep = 0

            self.sets[self.setIndex].patterns[self.patternIndex].steps[self.seqstep].selectedLayer[
                0] = self.lastUsedLayer

        elif action == "seqStepDown":
            # FIXME: move to sequencer
            # TODO: NCM
            self.seqstep -= self.stepSize

            if self.seqstep < 0:
                self.seqstep = self.sequencerSteps - self.stepSize

            # Set last used layer as active layer
            self.sets[self.setIndex].patterns[self.patternIndex].steps[self.seqstep].selectedLayer[
                0] = self.lastUsedLayer

        # Pattern Stepping
        elif action == "patternStepUp":
            if self.playing:
                self.patternChange += 1
            else:
                self.patternUp()

        elif action == "patternStepDown":
            if self.playing:
                self.patternChange -= 1
            else:
                self.patternDown()

        # Pattern mode switch
        elif action == "togglePatternMode":
            self.togglePatternMode()

        elif action == "toggleStep":
            self.sets[self.setIndex].patterns[self.patternIndex].steps[self.seqstep].toggleStep()

        # Play / Pause toggle
        elif action == "playPause":
            self.togglePlay()

        # note up/down
        elif action == "noteUp":
            self.noteUp()

        elif action == "noteDown":
            self.noteDown()

        # Note layer
        elif action == "layerUp":
            currentStep = self.sets[self.setIndex].patterns[self.patternIndex].steps[self.seqstep]
            currentStep.layerUp()  # TODO: when multiple NCMs are connected, add second variable to layerUpDown for selecting specific layer
            # (that's why selectedLayer[] is a list; first item = first NCM)

            self.sendMidi(True)
            self.lastUsedLayer = currentStep.selectedLayer[0]

        elif action == "layerDown":
            currentStep = self.sets[self.setIndex].patterns[self.patternIndex].steps[self.seqstep]
            currentStep.layerDown()

            self.sendMidi(True)
            self.lastUsedLayer = currentStep.selectedLayer[0]

        # Note Octave
        elif action == "octaveUp":
            currentStep = self.sets[self.setIndex].patterns[self.patternIndex].steps[self.seqstep]
            currentStep.noteLayers[currentStep.selectedLayer[0]].octaveUp()
            self.lastUsedOctave = currentStep.noteLayers[currentStep.selectedLayer[0]].octave

            self.sendMidi(True)

        elif action == "octaveDown":
            currentStep = self.sets[self.setIndex].patterns[self.patternIndex].steps[self.seqstep]
            currentStep.noteLayers[currentStep.selectedLayer[0]].octaveDown()
            self.lastUsedOctave = currentStep.noteLayers[currentStep.selectedLayer[0]].octave

            self.sendMidi(True)

        # MIDI channel
        elif action == "midiChannelUp":
            currentStep = self.sets[self.setIndex].patterns[self.patternIndex].steps[self.seqstep]
            currentStep.noteLayers[currentStep.selectedLayer[0]].channelUp()

            self.sendMidi(True)
            self.lastUsedMidiChannel = currentStep.noteLayers[
                currentStep.selectedLayer[0]].midiChannel  # TODO: multi NCM support

        elif action == "midiChannelDown":
            currentStep = self.sets[self.setIndex].patterns[self.patternIndex].steps[self.seqstep]
            currentStep.noteLayers[currentStep.selectedLayer[0]].channelDown()

            self.sendMidi(True)
            self.lastUsedMidiChannel = currentStep.noteLayers[
                currentStep.selectedLayer[0]].midiChannel  # TODO: multi NCM support

        # Sustain
        elif action == "toggleSustain":
            print("Toggling sustain")
            currentStep = self.sets[self.setIndex].patterns[self.patternIndex].steps[self.seqstep]
            currentStep.noteLayers[currentStep.selectedLayer[0]].toggleSustain()

        # Arm
        elif action == "toggleArm":
            print("Toggling arm")
            currentStep = self.sets[self.setIndex].patterns[self.patternIndex].steps[self.seqstep]
            currentStep.noteLayers[currentStep.selectedLayer[0]].toggleArm()

        # Save
        elif action == "save":
            self.save(self.saveIndex)

        elif action == "load":
            self.load(self.saveIndex)

        # Sustain
        elif action == "toggleSustain":
            currentStep = self.sets[self.setIndex].patterns[self.patternIndex].steps[self.seqstep]
            currentStep.noteLayers[currentStep.selectedLayer[0]].toggleSustain()

        # save up/down
        elif action == "saveUp":
            self.saveUp()
        # return "saveAnim"

        elif action == "saveDown":
            self.saveDown()
        # return "saveAnim"

        elif action == "setUp":
            if self.playing:
                self.setChange += 1
                self.clampPendingSetStepping()

            else:
                self.setUp()

        elif action == "setDown":
            if self.playing:
                self.setChange -= 1
                self.clampPendingSetStepping()

            else:
                self.setDown()

        elif action == "setRepeat":
            self.toggleSetRepeat()

        elif action == "prepareReset":
            if self.canReset:
                self.prepareReset = True


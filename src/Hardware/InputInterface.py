import config
from . import Debounce

# HW Enabled-specific stuff

if config.general['hardware_enabled']:
    from . import ShiftInput

    shiftInput = ShiftInput.ShiftInput()

    # DEBOUNCE
    # NCM 1
    noteUpDb = Debounce.Debounce()
    noteDownDb = Debounce.Debounce()
    layerUpDb = Debounce.Debounce()
    layerDownDb = Debounce.Debounce()
    octaveUpDb = Debounce.Debounce()
    octaveDownDb = Debounce.Debounce()
    channelUpDb = Debounce.Debounce()
    channelDownDb = Debounce.Debounce()
    sustainDb = Debounce.Debounce()
    armDb = Debounce.Debounce()

    # GCM buttons
    patternModeToggleDb = Debounce.Debounce()
    patternDownDb = Debounce.Debounce()
    stepDownDb = Debounce.Debounce()
    saveDownDb = Debounce.Debounce()
    saveUpDb = Debounce.Debounce()
    stepUpDb = Debounce.Debounce()
    patternUpDb = Debounce.Debounce()
    playDb = Debounce.Debounce()

    setDownDb = Debounce.Debounce()
    setUpDb = Debounce.Debounce()
    setRepeatDb = Debounce.Debounce()
    bpmUpDb = Debounce.Debounce()
    bpmDownDb = Debounce.Debounce()
    saveDb = Debounce.Debounce()
    loadDb = Debounce.Debounce()
    resetDb = Debounce.Debounce()


def readInputData() -> str:
    """ Handles inputs, returns action to be executed """

    # KEYBOARD INPUT
    # Quit
    # if char == ord('q'):
    #   return "quit"

    # # Reset
    # elif char == ord('r') or char == curses.KEY_RESIZE:
    #   return "reset"

    # # BPM up & down
    # elif char == ord('l'):
    #   return "bpmUp"

    # elif char == ord('k'):
    #   return "bpmDown"

    # # Sequencer stepping
    # elif char == ord('p'):
    #   return "seqStepUp"

    # elif char == ord('o'):
    #   return "seqStepDown"

    # # Pattern stepping
    # elif char == ord('m'):
    #   return "patternStepUp"

    # elif char == ord('n'):
    #   return "patternStepDown"

    # # Play / pausing (toggle)
    # elif char == ord(' '):
    #   return "playPause"

    # # Pattern Editing
    # elif char == ord('e'):
    #   return "patternEdit"

    # # Enable / Disable step
    # elif char == ord('d'):
    #   return "toggleStep"

    # # Show/hide keybinds
    # elif char == ord('z'):
    #   return "showKeys"

    # # Note up/down
    # elif char == ord('v'):
    #   return "noteUp"

    # elif char == ord('b'):
    #   return "noteDown"

    # # Layer up/down
    # elif char == ord('f'):
    #   return "layerUp"

    # elif char == ord('g'):
    #   return "layerDown"

    # # octave up/down
    # elif char == ord('x'):
    #   return "octaveUp"

    # elif char == ord('c'):
    #   return "octaveDown"

    # # pattern switch
    # elif char == ord('s'):
    #   return "togglePatternMode"

    # # sustain
    # elif char == ord('w'):
    #   return "toggleSustain"

    # # Save / load
    # elif char == ord('1'):
    #   return "save"     # TODO: multiple saves

    # elif char == ord('2'):
    #   return "load"

    # GPIO INPUT
    if config.general['hardware_enabled']:
        # GPIO Input String Layout:

        # 0: patternToggle
        # 1: pattern down
        # 2: step down
        # 3: save down
        # 4: save up
        # 5: step up
        # 6: pattern up
        # 7: play/pause

        # 8: set down
        # 9: reset
        # 10: bpm down
        # 11: save
        # 12: load
        # 13: bpm up
        # 14: set repeat
        # 15: set up

        # new mod
        # 16
        # 17
        # 18
        # 19
        # 20
        # 21
        # 22
        # 23

        # new mod 2
        # 24
        # 25
        # 26
        # 27
        # 28
        # 29
        # 30
        # 31

        # 32: noteLayerDown
        # 33: octaveDown
        # 34: midiChannelDown
        # 35: sustainDb
        # 36: noteModuleEnable/Arm
        # 37: midiChannelUp
        # 38: octaveUp
        # 39: noteLayerUp

        # 0: currentNoteUp
        # 1: currentNoteDown

        # Read inputs; set debouncing state
        hwInput = shiftInput.readData()

        btnCurrentNoteUp = hwInput[0]
        noteUpDb.setState(btnCurrentNoteUp, True)

        btnCurrentNoteDown = hwInput[1]
        noteDownDb.setState(btnCurrentNoteDown, True)

        btnNoteLayerDown = hwInput[2]
        layerDownDb.setState(btnNoteLayerDown, True)

        btnOctaveDown = hwInput[3]
        octaveDownDb.setState(btnOctaveDown, True)

        btnMidiChannelDown = hwInput[4]
        channelDownDb.setState(btnMidiChannelDown, True)

        btnSustain = hwInput[5]
        sustainDb.setState(btnSustain, True)

        btnArm = hwInput[6]
        armDb.setState(btnArm, True)

        btnMidiChannelUp = hwInput[7]
        channelUpDb.setState(btnMidiChannelUp, True)

        btnOctaveUp = hwInput[8]
        octaveUpDb.setState(btnOctaveUp, True)

        btnNoteLayerUp = hwInput[9]
        layerUpDb.setState(btnNoteLayerUp, True)

        btnPatternToggle = hwInput[10]
        patternModeToggleDb.setState(btnPatternToggle, True)

        btnPatternDown = hwInput[11]
        patternDownDb.setState(btnPatternDown, True)

        btnStepDown = hwInput[12]
        stepDownDb.setState(btnStepDown, True)

        btnSaveDown = hwInput[13]
        saveDownDb.setState(btnSaveDown, True)

        btnSaveUp = hwInput[14]
        saveUpDb.setState(btnSaveUp, True)

        btnStepUp = hwInput[15]
        stepUpDb.setState(btnStepUp, True)

        btnPatternUp = hwInput[16]
        patternUpDb.setState(btnPatternUp, True)

        btnPlay = hwInput[17]
        playDb.setState(btnPlay, True)

        btnSetDown = hwInput[18]
        setDownDb.setState(btnSetDown, True)

        btnReset = hwInput[19]
        resetDb.setState(btnReset, True)

        btnBpmDown = hwInput[20]
        bpmDownDb.setState(btnBpmDown, True)

        btnSave = hwInput[21]
        saveDb.setState(btnSave, True)

        btnLoad = hwInput[22]
        loadDb.setState(btnLoad, True)

        btnBpmUp = hwInput[23]
        bpmUpDb.setState(btnBpmUp, True)

        btnSetRepeat = hwInput[24]
        setRepeatDb.setState(btnSetRepeat, True)

        btnSetUp = hwInput[25]
        setUpDb.setState(btnSetUp, True)

        # Output returns
        if btnCurrentNoteUp == '1' and noteUpDb.checkDebounce():
            return "noteUp"

        elif btnCurrentNoteDown == '1' and noteDownDb.checkDebounce():
            return "noteDown"

        elif btnNoteLayerUp == '1' and layerUpDb.checkDebounce():
            return "layerUp"

        elif btnNoteLayerDown == '1' and layerDownDb.checkDebounce():
            return "layerDown"

        elif btnOctaveUp == '1' and octaveUpDb.checkDebounce():
            return "octaveUp"

        elif btnOctaveDown == '1' and octaveDownDb.checkDebounce():
            return "octaveDown"

        elif btnMidiChannelUp == '1' and channelUpDb.checkDebounce():
            return "midiChannelUp"

        elif btnMidiChannelDown == '1' and channelDownDb.checkDebounce():
            return "midiChannelDown"

        elif btnSustain == '1' and sustainDb.checkDebounce():
            return "toggleSustain"

        elif btnArm == '1' and armDb.checkDebounce():
            return "toggleArm"

        elif btnPatternToggle == '1' and patternModeToggleDb.checkDebounce():
            return "togglePatternMode"

        elif btnPatternDown == '1' and patternDownDb.checkDebounce():
            return "patternStepDown"

        elif btnPatternUp == '1' and patternUpDb.checkDebounce():
            return "patternStepUp"

        elif btnStepDown == '1' and stepDownDb.checkDebounce():
            return "seqStepDown"

        elif btnStepUp == '1' and stepUpDb.checkDebounce():
            return "seqStepUp"

        elif btnSaveDown == '1' and saveDownDb.checkDebounce():
            return "saveDown"

        elif btnSaveUp == '1' and saveUpDb.checkDebounce():
            return "saveUp"

        elif btnPlay == '1' and playDb.checkDebounce():
            return "playPause"

        elif btnSetDown == '1' and setDownDb.checkDebounce():
            return "setDown"

        elif btnSetUp == '1' and setUpDb.checkDebounce():
            return "setUp"

        elif btnSetRepeat == '1' and setRepeatDb.checkDebounce():
            return "setRepeat"

        elif btnBpmDown == '1' and bpmDownDb.checkDebounce():
            return "bpmDown"

        elif btnBpmUp == '1' and bpmUpDb.checkDebounce():
            print("bpmUp")
            return "bpmUp"

        elif btnSave == '1' and saveDb.checkDebounce():
            return "save"

        elif btnLoad == '1' and loadDb.checkDebounce():
            return "load"

        elif btnReset == '1' and resetDb.resetDebounce():
            print("doReset")
            return "doReset"

        elif btnReset == '1' and not resetDb.resetDebounce():
            return "prepareReset"

    return ""

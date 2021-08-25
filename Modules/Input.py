import curses 
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

def doInput(self, char):
  # Handles inputs, returns action to be executed
  # TODO: change to dynamic keyboard bindings thru config
  # TODO: hook up GPIO inputs

  # KEYBOARD INPUT
  # Quit
  if char == ord('q'):
    return "quit"
  
  # Reset
  elif char == ord('r') or char == curses.KEY_RESIZE:
    return "reset"

  # BPM up & down
  elif char == ord('l'):
    return "bpmUp"

  elif char == ord('k'):
    return "bpmDown"

  # Sequencer stepping
  elif char == ord('p'):
    return "seqStepUp"

  elif char == ord('o'):
    return "seqStepDown"

  # Pattern stepping
  elif char == ord('m'):
    return "patternStepUp"
  
  elif char == ord('n'):
    return "patternStepDown"

  # Play / pausing (toggle)
  elif char == ord(' '):
    return "playPause"

  # Pattern Editing
  elif char == ord('e'):
    return "patternEdit"

  # Enable / Disable step
  elif char == ord('d'):
    return "toggleStep"

  # Show/hide keybinds
  elif char == ord('z'):
    return "showKeys"

  # Note up/down
  elif char == ord('v'):
    return "noteUp"

  elif char == ord('b'):
    return "noteDown"

  # Layer up/down
  elif char == ord('f'):
    return "layerUp"

  elif char == ord('g'):
    return "layerDown"

  # octave up/down
  elif char == ord('x'):
    return "octaveUp"

  elif char == ord('c'):
    return "octaveDown"

  # pattern switch
  elif char == ord('s'):
    return "togglePatternMode"

  # sustain
  elif char == ord('w'):
    return "toggleSustain"

  # Save / load
  elif char == ord('1'):
    return "save"     # TODO: multiple saves
  elif char == ord('2'):
    return "load"

  # GPIO INPUT
  if config.general['hardware_enabled']: 
    # GPIO Input String Layout:
    # 0: currentNoteUp
    # 1: currentNoteDown
    # 2: noteLayerDown
    # 3: octaveDown
    # 4: midiChannelDown
    # 5: sustainDb
    # 6: noteModuleEnable/Arm
    # 7: midiChannelUp
    # 8: octaveUp
    # 9: noteLayerUp

    # 10: patternToggle
    # 11: pattern down
    # 12: step down
    # 13: save down
    # 14: save up
    # 15: step up
    # 16: pattern up
    # 17: play/pause

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
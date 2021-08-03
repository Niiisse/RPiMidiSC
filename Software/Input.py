import curses 
import config

if config.general['hardware_enabled']:
  from Hardware.ShiftInput import NoteModule
  noteModule = NoteModule()

class Input:
  char = None


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

  # GPIO INPUT
  if config.general['hardware_enabled']: 
    # GPIO Input String Layout (10 bits):
    # 0: currentNoteUp
    # 1: currentNoteDown
    # 2: noteLayerUp
    # 3: octaveDown
    # 4: midiChannelDown
    # 5: sustain
    # 6: noteModuleEnable/Arm
    # 7: midiChannelUp
    # 8: octaveUp
    # 9: noteLayerDown
    
    hwInput = noteModule.readData()
    
    btnCurrentNoteUp = hwInput[0]
    btnCurrentNoteDown = hwInput[1]
    btnNoteLayerUp = hwInput[2]
    btnOctaveDown = hwInput[3]
    btnMidiChannelDown = hwInput[4]
    btnSustain = hwInput[5]
    btnArm = hwInput[6]
    btnMidiChannelUp = hwInput[7]
    btnOctaveUp = hwInput[8]
    btnNoteLayerDown = hwInput[9]

    if btnCurrentNoteUp == '1':
      return "noteUp"
    elif btnCurrentNoteDown == '1':
      return "noteDown"
    elif btnNoteLayerUp == '1':
      return "layerUp"
    elif btnNoteLayerDown == '1':
      return "layerDown"
    elif btnOctaveUp == '1':
      return "octaveUp"
    elif btnOctaveDown == '1':
      return "octaveDown"
    elif btnMidiChannelUp == '1':
      return "midiChannelUp"
    elif btnMidiChannelDown == '1':
      return "midiChannelDown"
    elif btnSustain == '1':
      return "toggleSustain"
    elif btnArm == '1':
      return "toggleArm"

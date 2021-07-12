import curses
import config

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

  # GPIO INPUT
  if config.general['hardware_enabled']: 
    # TODO: Hardware inputs (do check if enabled first)
    return "notImplemented"
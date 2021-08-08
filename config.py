general = {
  "app_version": "v 0.2.3",     # General version nr
  "hardware_enabled": False,    # Whether to enable or disable the hardware interface
  "midiEnabled": False,         # Whether to enable MIDI output
  "blinkTime": 0.25             # Blinking time duration  
}

debounce = {
  # For debouncing hardware buttons

  "initialWait": 0.15, 
  "secondWait": 1,
  "thirdWait": 0.1
}

sequencer = {
  # Sequencer window

  "bpm": 120,                 # Tempo
  "seqstep": 0,               # Current step of sequencer
  "seqstepmax": 16,           # Total sequencer steps
  "seqstepsize": 1,           # Steps per step
  "begin_x": 23,              # Horizontal top-left
  "begin_y": 6,               # Vertical top-left
  "seqWinHeight": 9,          # Sequencer window height
  "seqWinWidth": 36,          # Sequencer window width
  "playing": True,            # Playing or paused
}

tempo = {
  # Tempo window

  "tempoWinHeight": 5,        # Height of tempo window
  "tempoWinWidth": 13         # Width of tempo window
}

status = {
  # Status Window

  "statusWinHeight": 5,       # Height of status window
  "statusWinWidth": 13        # Width of status window
}

pattern = {
  # Pattern Window

  "patternWinHeight": 6,      # Height of pattern window
  "patternWinWidth": 13,      # Width of pattern window
  "patternStep": 1,           # Current pattern step
  "patternAmount": 2,         # Max amount of patterns
  "patternMode": "auto"       # Auto mode makes pattern follow seqstep stuff
}

noteWindow = {
  # Note Window config 

  "noteWinHeight": 5,
  "noteWinWidth": 13,
}

interface = {
  # Interface options  FIXME: change to userInterface for clarity
  
  "drawKeybinds": False,      # Whether the UI should show keybinds
}
general = {
  "version": "v0.3.0",     # General version nr
  "hardware_enabled": True,    # Whether to enable or disable the hardware interface
  "midiEnabled": False,         # Whether to enable MIDI output
  "blinkTime": 0.25             # Blinking time duration
}

debounce = {
  # For debouncing hardware buttons

  "initialWait": 0.15,
  "secondWait": 1,
  "thirdWait": 0.1,
  "resetWait": 3
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
  "playing": False,            # Playing or paused
  "previewNoteDuration": 0.5  # How long a previewNote should play for
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
  # Pattern

  "patternWinHeight": 6,      # Height of pattern window
  "patternWinWidth": 13,      # Width of pattern window
  "patternIndex": 1,           # Current pattern step
  "patternAmount": 16,         # Max amount of patterns
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

misc = {
  "hw_off_string": "11111111111111111111111111111110111111100000000000000000111111101111111011111110111111100000000001111111",
  "hw_crash_string": "10101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101001111111",
  "resetString":   "11111111111111111111111100000000000000001100110000110011111111101111111000000000000000000010000000000000"
}

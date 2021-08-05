import curses, traceback
from curses import wrapper
from curses.textpad import Textbox, rectangle
import time
import math
import config

from . import Input
from . import Blink
from . import Sequencer

# User Interface class
#
# Handles, well, user interface. Reports program state back to main with a return.

class Ui:
	def __init__(self, midi):
		self.midi = midi

	app_version = config.general['app_version']
	outputByteString = "no data"

	seqWinHeight = config.sequencer['seqWinHeight']
	seqWinWidth = config.sequencer['seqWinWidth']
	tempoWinHeight = config.tempo['tempoWinHeight'] 
	tempoWinWidth = config.tempo['tempoWinWidth']
	tempoWinSize = (config.tempo['tempoWinHeight'], config.tempo['tempoWinWidth'])
	statusWinSize = (config.status['statusWinHeight'], config.status['statusWinWidth'])
	patternWinSize = (config.pattern['patternWinHeight'], config.pattern['patternWinWidth'])
	patternMode = config.pattern['patternMode']
	patternAmount = config.pattern['patternAmount']
	showKeyBinds = config.interface['drawKeybinds']
	keysLastFrame = False

	keyBinds = (
		"q: quit",
		"r: reset",
		"k / l: bpm",
		"o / p: step",
		"n / m: pattern",
		"space: play/pause",
		"e: pattern edit",
		"d: toggle step",
		"z: show/hide keybinds"
	)

	seqwin = None
	tempoWin = None
	statusWin = None
	patternWin = None
	window = None
	char = None
	sequencer = None

	blink = Blink.Blink(config.general['blinkTime'])
	sequencer = Sequencer.Sequencer(config.pattern['patternAmount'], config.sequencer['seqstepmax'], config.sequencer['bpm'], config.sequencer['seqstepsize'])
	
def main():
	# Sets up main window

	doWindowSetup() # Initial curses setup

	drawTitle()

	# Get window size, use it to set up subwindows
	windowSize = Ui.window.getmaxyx()

	createSequencerWindow(windowSize)
	createTempoWindow(windowSize)
	createStatusWindow(windowSize)
	createPatternWindow(windowSize)
	
def updateUi():
	# Main UI loop. Handles inputs, then updates windows
	
	# Clamps for keeping various vars within bounds
	#clampSequencerStep(Ui.sequencer) 		# TODO: move to Sequencer, create some Sequencer.update def. 
																			# That update call prolly shouldn't be in UI, either.
	#Ui.sequencer.stepSequencer() 				# TODO: move to update function in seq
	clampPatternStepping(Ui.sequencer)
	clampPendingStepping(Ui.sequencer)

	# Drawing, updating subwindows + associated processing
	drawInfo(Ui.seqwin, Ui.sequencer)
	drawTempoWindow(Ui.tempoWin)
	drawStatusWindow(Ui.statusWin, Ui.sequencer)
	drawPatternWindow(Ui.patternWin, Ui.sequencer)
	drawSequencer(Ui.seqwin, Ui.sequencer)										# Draws sequencer
	Ui.sequencer.timer()													# Manages sequencer timer
	#drawDebugBar(Ui.window, Ui.outputByteString)							# Draws debug bar

	Ui.keysLastFrame = drawKeybinds(Ui.window, Ui.showKeyBinds, Ui.keysLastFrame, Ui.keyBinds)	# Draws the keyBindings, clears it only when necessary

	Ui.window.refresh()
	Ui.seqwin.refresh()
	Ui.tempoWin.refresh()
	Ui.statusWin.refresh()
	Ui.patternWin.refresh()

	# Generate output bytestring, process inputs for next frame
	# pass outputByteString to processInput to return the bytestring to main.py, assuming no other
	# events have priority.

	Ui.outputByteString = createOutputString(Ui.sequencer)
	return processInput(Ui.outputByteString, Ui.sequencer)

##
## UI Creation and Drawing / Updating
##
		
def createSequencerWindow(windowSize):
	# draw Sequencer Window in the middle of the screen

	begin_y = math.floor(windowSize[0] / 2 - Ui.seqWinHeight / 2)
	begin_x = math.floor(windowSize[1] / 2 - Ui.seqWinWidth / 2)

	Ui.seqwin = curses.newwin(Ui.seqWinHeight, Ui.seqWinWidth, begin_y, begin_x)
	Ui.seqwin.border()
	Ui.seqwin.addstr(0, 2, "   SEQUENCER   ", curses.A_BOLD | curses.A_REVERSE)	# Title
	Ui.start_timer = True

def createTempoWindow(windowSize):
	# draw BPM window left of seqWin
	#TODO: check for space, otherwise put it above or below or something

	seqSize = Ui.seqwin.getmaxyx()

	# Y position is (for now) middle of screen - own height. X position is half of screen - seqwin width
	begin_y = math.floor(windowSize[0] / 2 - Ui.tempoWinSize[0] - 1)
	begin_x = math.floor((windowSize[1] / 2 - Ui.tempoWinSize[1]) - seqSize[1] / 2) - 1

	Ui.tempoWin = curses.newwin(Ui.tempoWinHeight, Ui.tempoWinWidth, begin_y, begin_x)
	Ui.tempoWin.border()
	Ui.tempoWin.addstr(0, 2, "  Tempo  ", curses.A_BOLD | curses.A_REVERSE) 

def createStatusWindow(windowSize):
	seqSize = Ui.seqwin.getmaxyx()

	begin_y = math.floor(windowSize[0] / 2 - Ui.statusWinSize[0] / 2)
	begin_x = math.floor(windowSize[1] / 2 + seqSize[1] / 2) + 1

	Ui.statusWin = curses.newwin(Ui.statusWinSize[0], Ui.statusWinSize[1], begin_y, begin_x)
	Ui.statusWin.border()
	Ui.statusWin.addstr(0, 2, " Status  ", curses.A_BOLD | curses.A_REVERSE)

def createPatternWindow(windowSize):
	seqSize = Ui.seqwin.getmaxyx()

	begin_y = math.floor(windowSize[0] / 2 + Ui.tempoWinSize[0] / 2 - Ui.patternWinSize[0] / 2)
	begin_x = math.floor(windowSize[1] / 2 - seqSize[1] / 2 - Ui.patternWinSize[1]) - 1

	Ui.patternWin = curses.newwin(Ui.patternWinSize[0], Ui.patternWinSize[1], begin_y, begin_x)
	Ui.patternWin.border()
	Ui.patternWin.addstr(0, 2, " Pattern ", curses.A_BOLD | curses.A_REVERSE)

def drawSequencer(seqwin, sequencer):
	# Draws main sequencer.
	# states:
	#		Playing mode. Either playing or paused. Current step is highlighted.
	#		Editing mode. All steps are highlighted. Current step blinks. 
	#
	# FIXME: this works currently because I don't use other color pairs, but I shouldn't define them here.

	curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)		# Active Seq color pair
	curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)		# Inactive Seq color pair
	curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLACK)		# Disabled Seq color pair
	curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_GREEN)		# Enabled selected in Editing
	curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_GREEN)		# Enabled selected in Editing

	halfSteps = math.floor(sequencer.sequencerSteps / 2)					# Makes life easier

	# state is playing or paused, but overridden by editing. State is used to determine drawing mode.
	if sequencer.patternEditing:
		state = "editing"
	else:
		state = "playing" if sequencer.playing else "paused"

	# PLAY MODE DRAWING #

	if state == "playing" or state == "paused":

		# Double for loop for playing mode. patternAmount + 1 because we have an empty row
		for y in range(5):
			for x in range(halfSteps):
				
				dX = 2 + x  * 4														# d(raw)X. + 2 because we want it to draw inside the window, not on the edge
				dY = 2 + y																# d(raw)Y. Same story here
				colorPair = curses.color_pair(2)					# Default to non-selected color pair
				modifier = curses.A_BOLD									# Probably unnecessary due to me changing my mind
				drawStep = sequencer.seqstep							# Used for the second row. Easier than typing "seqstep/2" all the time
				drawString = "****"
				xStep = x if y < 2 else x+halfSteps				# Doubles if we're in the second row
				
				# Drawstep logic (used for highlighting second row). 
				if sequencer.seqstep >= halfSteps:
					drawStep = sequencer.seqstep - halfSteps

				# Color selecting for first row
				if sequencer.seqstep < halfSteps:
					if x == drawStep and y < 2:
						colorPair = curses.color_pair(1)

				# Second row color selecting
				elif sequencer.seqstep >= halfSteps:
					if x == drawStep and y > 2:
						colorPair = curses.color_pair(1)
				
				if sequencer.patterns[sequencer.patternStep].patternSteps[xStep].getState() == False:
					drawString = "    "

				# Finally! Draw the *, but don't draw 3rd line
				if y != 2:
					seqwin.addstr(dY, dX, drawString, colorPair | modifier)


	# EDITING MODE DRAWING #

	elif state == "editing":
		
		for y in range(5):
			for x in range(halfSteps):
				
				dX = 2 + x*4															# d(raw)X. + 2 because we want it to draw inside the window, not on the edge
				dY = 2 + y																# d(raw)Y. Same story here
				colorPair = curses.color_pair(1)					# Default to selected color pair
				modifier = curses.A_BOLD									# Modifier for string
				drawStep = sequencer.seqstep							# Used for the second row. Easier than typing "seqstep/2" all the time
				xStep = x if y < 2 else x+halfSteps				# Doubles if we're in the second row
				selectedState = True											# Used for seeing if the selected step is enabled/disabled

				#  Drawstep logic
				if sequencer.seqstep >= halfSteps:
					drawStep = sequencer.seqstep - halfSteps

				# Color selecting for first row
				if y < 2:
					if sequencer.patterns[sequencer.patternStep].patternSteps[xStep].getState() == False:
						colorPair = curses.color_pair(3)
						selectedState = False

					# Current step selected?
					if sequencer.seqstep < halfSteps and x == drawStep:

						# Determine color pair
						if selectedState:
							colorPair = curses.color_pair(4)
						else:
							colorPair = curses.color_pair(5)

				# Second row color selecting
				elif y > 2:
					if sequencer.patterns[sequencer.patternStep].patternSteps[xStep].getState() == False:
						colorPair = curses.color_pair(3)
						modifier = curses.A_NORMAL
						selectedState = False

					# Current step?
					if sequencer.seqstep >= halfSteps and x == drawStep:

						# Determine color
						if selectedState:
							colorPair = curses.color_pair(4)
						else:
							colorPair = curses.color_pair(5)

				# Finally! Draw the *, but don't draw 3rd line
				if y != 2:
					seqwin.addstr(dY, dX, "****", colorPair | modifier)

def drawTempoWindow(tempoWin):
	# Draws contents of tempo window

	# First string clears line. Second paints bold text. Third paints BPM. 
	tempoWin.addstr(2, 7, "   ", curses.A_NORMAL)
	tempoWin.addstr(2, 7, "{}".format(Ui.sequencer.bpm), curses.A_BOLD)
	tempoWin.addstr(2, 3, "BPM ", curses.A_NORMAL)

def drawStatusWindow(statusWin, sequencer):
	# Draws statuswin contents
	if sequencer.patternEditing:
		statusWin.addstr(2, 3, "Editing", curses.A_BOLD | curses.A_BLINK)
	
	else:
		if sequencer.playing:
			statusWin.addstr(2, 3, "Playing", curses.A_BOLD)
		
		else:
			statusWin.addstr(2, 3, "Pausing", curses.A_NORMAL | curses.A_BLINK)

def drawPatternWindow(patternWin, sequencer):
	# Function for filling pattern window contents

	# Logic for deciding whether resultingString should blink (if there's a pattern change upcoming)
	if sequencer.patternChange != 0:
		stringModifier = curses.A_BOLD | curses.A_BLINK
		patternStepString = "{}".format(sequencer.pendingPattern)

	else:
		stringModifier = curses.A_BOLD
		patternStepString = "{}".format(sequencer.patternStep)

	# Some logic for deciding whether a 0 needs to be added for visual purposes
	patternMaxString = "{}".format(sequencer.patternAmount)
	
	if sequencer.patternStep <= 9:
		patternStepString = "0" + patternStepString
	
	if sequencer.patternAmount <= 9:
		patternMaxString = "0" + patternMaxString

	resultingString = patternStepString + " / " + patternMaxString

	patternWin.addstr(2, 3, resultingString, stringModifier)

def drawTitle():
	# Function for drawing the window title, figuring out where it's supposed to go

	titleString = "   RPi MIDI Controller / Sequencer {}   ".format(Ui.app_version)
	titleLength = len(titleString)
	screenPos = Ui.window.getmaxyx()

	width = math.floor(screenPos[1] / 2 - titleLength / 2)
	Ui.window.addstr(0, width, titleString, curses.A_REVERSE | curses.A_BOLD)

def drawInfo(seqwin, sequencer):
	# Draws some (prolly temporary) info
	seqwin.addstr(0, 25, " step:    ", curses.A_ITALIC)								
	seqwin.addstr(0, 25, " step: {} ".format(sequencer.seqstep), curses.A_ITALIC)									# Show seq step
	# UI.window.addstr(3, 1, " BPM:    ".format(UI.seqstep), curses.A_ITALIC)										# Fix bug
	# UI.window.addstr(3, 1, " BPM: {} ".format(UI.gv.bpm), curses.A_ITALIC | curses.A_DIM)			# Show BPM

def drawDebugBar(window, byteString):
	# Draws debug bar if there is enough room
	size = window.getmaxyx()
	stringLength = len(byteString)

	# Check if it fits, otherwise just don't paint it 
	if stringLength + 6 <= size[1]:
		byteString = "   " + byteString + "   "		
		width = math.floor(size[1] / 2 - (stringLength + 6) / 2)
		try:
			window.addstr(size[0]-1, width, byteString, curses.A_REVERSE | curses.A_BOLD)
		except:
			pass

def drawKeybinds(window, showKeyBinds, lastFrame, keyBinds):
	# keyBinds holds list of strings with keybinds
	# lastFrame holds bool of whether the list was drawn last frame.
	# if it was, and now no longer is, need to clear the old strings because curses

	if showKeyBinds:
		window.addstr(2, 2, " "*16, curses.A_NORMAL)
		for i, val in enumerate(keyBinds):
			window.addstr(i+2, 2, val, curses.A_ITALIC)
	
		return True

	else:
		if lastFrame:
			# Need to clear the screen

			for i, val in enumerate(keyBinds):
				window.addstr(i+2, 2, " "*len(val), curses.A_ITALIC)

			return False

		window.addstr(2, 2, "Show keybinds: z", curses.A_ITALIC)
		return False
		
##
## Program Logic
##

def getSequencer():
	return Ui.sequencer

def processInput(outputByteString, sequencer):
	# Process input events sent by Input
	action = Input.doInput(Input, Ui.window.getch())

	# Quit
	if action == "quit":
		restoreScreen()
		return "quit"

	# Reset
	elif action == "reset":
		return "reset"
	
	# BPM up & down; clamping
	elif action == "bpmUp":
		if sequencer.bpm < 999:
			sequencer.bpm += 1
		else:
			sequencer.bpm = 1

	elif action == "bpmDown":
		if sequencer.bpm > 1:
			sequencer.bpm -= 1
		else:
			sequencer.bpm = 999


	# Sequencer stepping next & previous; clamping
	elif action == "seqStepUp":
		sequencer.seqstep += sequencer.stepSize
		
		if sequencer.seqstep > sequencer.sequencerSteps - sequencer.stepSize:
			sequencer.seqstep = 0

	elif action == "seqStepDown":
		sequencer.seqstep -= sequencer.stepSize

		if sequencer.seqstep < 0:
			sequencer.seqstep = sequencer.sequencerSteps - sequencer.stepSize
	

	# Pattern Stepping
	elif action == "patternStepUp":
		sequencer.patternChange += 1
	elif action == "patternStepDown":
		sequencer.patternChange -= 1

	# Pattern Editing
	elif action == "patternEdit":
		sequencer.toggleEditMode()

	elif action == "toggleStep":
		sequencer.patterns[sequencer.patternStep].patternSteps[sequencer.seqstep].toggleStep()

	# Play / Pause toggle
	elif action == "playPause":
		if sequencer.patternEditing == False:
			sequencer.togglePlay()

	# Show keybinds
	elif action == "showKeys":
		Ui.showKeyBinds = False if Ui.showKeyBinds else True

	# note up/down
	elif action == "noteUp":
		currentStep = sequencer.patterns[sequencer.patternStep].patternSteps[sequencer.seqstep]
		currentStep.noteLayers[currentStep.selectedLayer[0]].noteUp()
		
		sequencer.sendMidi()

	elif action == "noteDown":
		currentStep = sequencer.patterns[sequencer.patternStep].patternSteps[sequencer.seqstep]
		currentStep.noteLayers[currentStep.selectedLayer[0]].noteDown()
	
		sequencer.sendMidi()
		
	# Note layer
	elif action == "layerUp":
		currentStep = sequencer.patterns[sequencer.patternStep].patternSteps[sequencer.seqstep]
		currentStep.layerUp() # TODO: when multiple NCMs are connected, add second variable to layerUpDown for selecting specific layer
													# (that's why selectedLayer[] is a list; first item = first NCM)

	elif action == "layerDown":
		currentStep = sequencer.patterns[sequencer.patternStep].patternSteps[sequencer.seqstep]
		currentStep.layerDown()

	# Note Octave
	elif action == "octaveUp":
		currentStep = sequencer.patterns[sequencer.patternStep].patternSteps[sequencer.seqstep]
		currentStep.noteLayers[currentStep.selectedLayer[0]].octaveUp()

	elif action == "octaveDown":
		currentStep = sequencer.patterns[sequencer.patternStep].patternSteps[sequencer.seqstep]
		currentStep.noteLayers[currentStep.selectedLayer[0]].octaveDown()

	# MIDI channel
	elif action == "midiChannelUp":
		currentStep = sequencer.patterns[sequencer.patternStep].patternSteps[sequencer.seqstep]
		currentStep.noteLayers[currentStep.selectedLayer[0]].channelUp()

	elif action == "midiChannelDown":
		currentStep = sequencer.patterns[sequencer.patternStep].patternSteps[sequencer.seqstep]
		currentStep.noteLayers[currentStep.selectedLayer[0]].channelDown()

	# Sustain
	elif action == "toggleSustain":
		currentStep = sequencer.patterns[sequencer.patternStep].patternSteps[sequencer.seqstep]
		currentStep.noteLayers[currentStep.selectedLayer[0]].toggleSustain()

	return outputByteString

def clampPatternStepping(sequencer):
	# Clamps pattern step

	if sequencer.patternStep > sequencer.patternAmount:
		sequencer.patternStep = 1
	elif sequencer.patternStep < 1:
		sequencer.patternStep = Ui.patternAmount

def clampPendingStepping(sequencer):
	# Calculate pending pattern stepping. Basically a fancy clamp

	if sequencer.patternChange != 0:																
		if sequencer.patternChange > sequencer.patternAmount - sequencer.patternStep:		
			sequencer.patternChange -= sequencer.patternAmount													

		if sequencer.patternChange + sequencer.patternStep < 1:
			sequencer.patternChange += sequencer.patternAmount

	sequencer.pendingPattern = sequencer.patternStep + sequencer.patternChange

def createOutputString(sequencer):
	# Creates output bytestring that can be sent to Hardware Interface
	
	# BPM #

	bpmString = format(sequencer.bpm)
	bpmOutput = ""

	while len(bpmString) < 3:					# Because format is '090', not '90'
		bpmString = "0" + bpmString

	for i in range(3):								# Sends individual number off to get the bytestring
		tempString = convertDecimalToByteString(int(bpmString[i]))
		bpmOutput = bpmOutput + tempString

	# PATTERN STEP #

	# Decide whether we should show actual step or pending step
	patternStepString = format(sequencer.patternStep) if sequencer.patternChange == 0 else format(sequencer.pendingPattern)

	while len(patternStepString) < 2:
		patternStepString = "0" + patternStepString

	patternStepOutput = ""

	for i in range(2):
		tempString = convertDecimalToByteString(int(patternStepString[i]))
		patternStepOutput = patternStepOutput + tempString

	# Should we blink?
	if sequencer.patternChange != 0:
		patternStepOutput = Ui.blink.blink(patternStepOutput, True)

	# SEQUENCER STEP #

	ledStep = sequencer.seqstep

	ledString = ""
	ledState = ""
	
	for i in range(sequencer.sequencerSteps):
		# Gon explain this one in detail cus ternary statements can be confusing to read
		# Loop over all steps in current Pattern
		# ledState sets what the potential state is going to be if this is the selected step.
		#
		# If editing:
		#		BLINK current step LED; else
		#		all LEDs ON; disabled steps: LED OFF
		#
		# If playing:
		#		all LEDs OFF, current step: LED ON
		#		pausing: BLINK current LED

		if sequencer.patternEditing:
			if i == ledStep:
				ledState = Ui.blink.blink("1", False)
			else:
				ledState = "1" if sequencer.patterns[sequencer.patternStep].patternSteps[i].getState() else "0"
	
		# playing mode
		else:
			if i == ledStep:
				if sequencer.patterns[sequencer.patternStep].patternSteps[i].getState():
					ledState = "1" if sequencer.playing == True else Ui.blink.blink("1", False)
				else:
					ledState = Ui.blink.blink("1", False) if sequencer.playing == False else "0"
			else:
				ledState = "0"
				 
		ledString += ledState

	# NOTEMODULE #
	# TODO: set last layerString bit correctly

	noteString = "11111110"
	layerString = "11111110"
	octaveString = "11111110"
	channelString = "11111111"

	currentStep = sequencer.patterns[sequencer.patternStep].patternSteps[sequencer.seqstep]

	noteString = convertDecimalToNote(currentStep.noteLayers[currentStep.selectedLayer[0]].note)	# TODO: this 0 would be replaced with i for note control modules
	layerString = convertDecimalToByteString(currentStep.selectedLayer[0])

	if currentStep.noteLayers[currentStep.selectedLayer[0]].note != 0: 
		# Checks whether it should display the values or write - (in case of disabled note)

		octaveString = convertDecimalToByteString(currentStep.noteLayers[currentStep.selectedLayer[0]].octave)
		channelString = convertDecimalToByteString(currentStep.noteLayers[currentStep.selectedLayer[0]].midiChannel)

	else:
		octaveString = "11111111"
		channelString = "11111111"

	# Note layer bit
	layerString = layerString[:-1] + '0'

	if currentStep.checkOtherLayers():
		layerString = layerString[:-1] + '1'

	# Sustain Bit
	if currentStep.noteLayers[currentStep.selectedLayer[0]].sustain:
		octaveString = octaveString[:-1] + '1'
	else:
		octaveString = octaveString[:-1] + '0'

	# OUTPUT #
	 
	return bpmOutput + patternStepOutput + ledString + noteString + layerString + octaveString + channelString

def convertDecimalToByteString(decimal):
	# Used for creating the outputbytestring

	numericArr = [        # Stores the numeric display bytes
	0b10000001,
	0b11101101,
	0b01000011,
	0b01001001,
	0b00101101,
	0b00011001,
	0b00010001,
	0b11001101,
	0b00000001,
	0b00001001
	]

	byteString = format(numericArr[decimal], '08b')

	return byteString

def convertDecimalToNote(decimal):
	# Used for converting note number to actual note

	noteArr = [        # Stores the numeric display bytes
	0b01111110,		# -
	0b01110010,		# C
	0b01110011,		# C#
	0b01100000,		# D
	0b01100001,		# D#
	0b00010010,		# E
	0b00010110,		# F
	0b00010111,		# F#
	0b10010000,		# G
	0b10010001,		# G#
	0b00000100,		# A
	0b00000101,		# A#
	0b00110000,		# B
	]

	byteString = format(noteArr[decimal], '08b')

	return byteString

##
## Curses Starting & Resetting 
##

def doWindowSetup():
	# Initializes curses and the main window

	Ui.window = curses.initscr()

	curses.noecho()
	curses.cbreak()
	curses.curs_set(0)
	curses.start_color()
	
	Ui.window.clear()            # Clears the screen
	Ui.window.nodelay(True)
	Ui.window.border()

def restoreScreen():
	curses.nocbreak()
	curses.echo()
	curses.endwin()

def resetScreen():
	# Resets the screen, aids with getting the right terminal window

	restoreScreen()
	curses.endwin()

def startUI():
	try: 
		main()
	except:
		restoreScreen()
		traceback.print_exc()
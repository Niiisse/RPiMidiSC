import curses, traceback
from curses.textpad import Textbox, rectangle
from curses import wrapper
from . import Input
from . import GlobalVars
import time
import math
import config

# TODO: debugging window thingy for putting vars in
# Could make a little command like structure like in vim; show bar on bottom of screen
# and have a key1+key2 for selecting focus of debug output var

class UI:
	app_version = config.general['app_version']

	seqstep = 0																	
	seqstepmax = config.sequencer['seqstepmax']
	seqstepsize = config.sequencer['seqstepsize']

	seqWinHeight = config.sequencer['seqWinHeight']
	seqWinWidth = config.sequencer['seqWinWidth']
	tempoWinHeight = config.tempo['tempoWinHeight'] 
	tempoWinWidth = config.tempo['tempoWinWidth']
	tempoWinSize = (config.tempo['tempoWinHeight'], config.tempo['tempoWinWidth'])
	statusWinSize = (config.status['statusWinHeight'], config.status['statusWinWidth'])
	patternWinSize = (config.pattern['patternWinHeight'], config.pattern['patternWinWidth'])
	patternMode = config.pattern['patternMode']
	patternMax = config.pattern['patternMax']

	seqwin = None
	tempoWin = None
	statusWin = None
	patternWin = None
	window = None
	start_timer = True
	char = None
	tic = None

	gv = GlobalVars.GlobalVars()
	gv.bpm = config.sequencer['bpm']
	gv.playing = config.sequencer['playing']
	gv.patternStep = config.pattern['patternStep']

def main():
	# Sets up main window

	doWindowSetup() # Initial curses setup

	drawTitle()

	# Get window size, use it to set up subwindows
	windowSize = UI.window.getmaxyx()

	createSequencerWindow(windowSize)
	createTempoWindow(windowSize)
	createStatusWindow(windowSize)
	createPatternWindow(windowSize)
	
def update_ui():
	# Main UI loop. Handles inputs, then updates windows
	
	# Clamps for keeping various vars within bounds
	UI.seqstep = clampSequencerStep(UI.seqstep)
	clampPatternStepping()
	clampPendingStepping()

	# Drawing, updating subwindows + associated processing
	drawInfo()
	drawTempoWindow(UI.tempoWin)
	drawStatusWindow(UI.statusWin, UI.gv.playing)
	drawPatternWindow(UI.patternWin, UI.gv.patternStep, UI.patternMax)
	drawSequencer(UI.seqwin, UI.seqstep)																											# Draw sequencer
	sequencerTimer() 	# Manages sequencer timer

	UI.window.refresh()
	UI.seqwin.refresh()
	UI.tempoWin.refresh()
	UI.statusWin.refresh()
	UI.patternWin.refresh()

	# Return new sequencer step to global var
	UI.gv.setSeqstep(UI.seqstep)
	UI.gv.setBPM(UI.gv.bpm)

	# Process inputs (for next frame)
	return processInput()


## UI Creation and Drawing
				
def createSequencerWindow(windowSize):
	# draw Sequencer Window in the middle of the screen

	begin_y = math.floor(windowSize[0] / 2 - UI.seqWinHeight / 2)
	begin_x = math.floor(windowSize[1] / 2 - UI.seqWinWidth / 2)

	UI.seqwin = curses.newwin(UI.seqWinHeight, UI.seqWinWidth, begin_y, begin_x)
	UI.seqwin.border()
	UI.seqwin.addstr(0, 2, "   SEQUENCER   ", curses.A_BOLD | curses.A_REVERSE)	# Title
	UI.start_timer = True

def createTempoWindow(windowSize):
	# draw BPM window left of seqWin
	#TODO: check for space, otherwise put it above or below or something

	seqSize = UI.seqwin.getmaxyx()

	# Y position is (for now) middle of screen - own height. X position is half of screen - seqwin width
	begin_y = math.floor(windowSize[0] / 2 - UI.tempoWinSize[0] - 1)
	begin_x = math.floor((windowSize[1] / 2 - UI.tempoWinSize[1]) - seqSize[1] / 2) - 1

	UI.tempoWin = curses.newwin(UI.tempoWinHeight, UI.tempoWinWidth, begin_y, begin_x)
	UI.tempoWin.border()
	UI.tempoWin.addstr(0, 2, "  Tempo  ", curses.A_BOLD | curses.A_REVERSE) 

def createStatusWindow(windowSize):
	seqSize = UI.seqwin.getmaxyx()

	begin_y = math.floor(windowSize[0] / 2 - UI.statusWinSize[0] / 2)
	begin_x = math.floor(windowSize[1] / 2 + seqSize[1] / 2) + 1

	UI.statusWin = curses.newwin(UI.statusWinSize[0], UI.statusWinSize[1], begin_y, begin_x)
	UI.statusWin.border()
	UI.statusWin.addstr(0, 2, " Status  ", curses.A_BOLD | curses.A_REVERSE)

def createPatternWindow(windowSize):
	seqSize = UI.seqwin.getmaxyx()

	begin_y = math.floor(windowSize[0] / 2 + UI.tempoWinSize[0] / 2 - UI.patternWinSize[0] / 2)
	begin_x = math.floor(windowSize[1] / 2 - seqSize[1] / 2 - UI.patternWinSize[1]) - 1

	UI.patternWin = curses.newwin(UI.patternWinSize[0], UI.patternWinSize[1], begin_y, begin_x)
	UI.patternWin.border()
	UI.patternWin.addstr(0, 2, " Pattern ", curses.A_BOLD | curses.A_REVERSE)

def drawSequencer(seqwin, seqstep):
	# Draws main sequencer

	curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)		# Active Seq color pair
	curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)		# Inactive Seq color pair

	for y in range(5):
		for x in range(32):
			draw_x = 2 + x
			draw_y = 2 + y
			drawstep = UI.seqstep

			# Setting Color Logic
			color_pair = curses.color_pair(2)

			if UI.seqstep >= 32:																							# Drawstep is used for second row highlighting
				drawstep = UI.seqstep - (UI.seqstepmax/2)

			if UI.seqstep <= 31:																							# First 32 steps = first row	
				if x >= drawstep and x <= drawstep + 1 and y < 2:
					color_pair = curses.color_pair(1)

			elif UI.seqstep >= 30:																						# Second 32 steps = second row
				if x >= drawstep and x <= drawstep + 1 and y > 2:						
					color_pair = curses.color_pair(1)

			if y != 2:																												# Make sure there's a blank line inbetween
				UI.seqwin.addstr(draw_y, draw_x, "*", color_pair | curses.A_BOLD)		# Draw the seq chars

def drawTempoWindow(tempoWin):
	# Draws contents of tempo window

	# First string clears line. Second paints bold text. Third paints BPM. 
	tempoWin.addstr(2, 7, "   ", curses.A_NORMAL)
	tempoWin.addstr(2, 7, "{}".format(UI.gv.bpm), curses.A_BOLD)
	tempoWin.addstr(2, 3, "BPM ", curses.A_NORMAL)

def drawStatusWindow(statusWin, playing):
	# Draws statuswin contents

	if playing:
		statusWin.addstr(2, 3, "Playing", curses.A_BOLD)
	
	else:
		statusWin.addstr(2, 3, "Pausing", curses.A_NORMAL | curses.A_BLINK)

def drawPatternWindow(patternWin, patternStep, patternMax):
	# Function for filling pattern window contents

	# Logic for deciding whether resultingString should blink (if there's a pattern change upcoming)
	if UI.gv.patternChange != 0:
		stringModifier = curses.A_BOLD | curses.A_BLINK
		patternStepString = "{}".format(UI.gv.patternPending)

	else:
		stringModifier = curses.A_BOLD
		patternStepString = "{}".format(patternStep)

	# Some logic for deciding whether a 0 needs to be added for visual purposes
	patternMaxString = "{}".format(patternMax)
	
	if patternStep <= 9:
		patternStepString = "0" + patternStepString
	
	if patternMax <= 9:
		patternMaxString = "0" + patternMaxString

	resultingString = patternStepString + " / " + patternMaxString

	patternWin.addstr(2, 3, resultingString, stringModifier)

def drawTitle():
	# Function for drawing the window title, figuring out where it's supposed to go

	titleString = "   RPi MIDI Controller / Sequencer {}   ".format(UI.app_version)
	titleLength = len(titleString)
	screenPos = UI.window.getmaxyx()

	width = math.floor(screenPos[1] / 2 - titleLength / 2)
	UI.window.addstr(0, width, titleString, curses.A_REVERSE | curses.A_BOLD)

def drawInfo():
	# Draws some (prolly temporary) info
	UI.seqwin.addstr(0, 25, " step:    ", curses.A_ITALIC)								
	UI.seqwin.addstr(0, 25, " step: {} ".format(UI.seqstep), curses.A_ITALIC)									# Show seq step
	# UI.window.addstr(3, 1, " BPM:    ".format(UI.seqstep), curses.A_ITALIC)										# Fix bug
	# UI.window.addstr(3, 1, " BPM: {} ".format(UI.gv.bpm), curses.A_ITALIC | curses.A_DIM)			# Show BPM


## Program Logic

def processInput():
	# Process input events sent by Input
	action = Input.doInput(Input, UI.window.getch())

	# Quit
	if action == "quit":
		restoreScreen()
		return "quit"

	# Reset
	elif action == "reset":
		return "reset"

	
	# BPM up & down; clamping
	elif action == "bpmUp":
		if UI.gv.bpm < 999:
			UI.gv.bpm += 1
		else:
			UI.gv.bpm = 0

	elif action == "bpmDown":
		if UI.gv.bpm > 0:
			UI.gv.bpm -= 1
		else:
			UI.gv.bpm = 999


	# Sequencer stepping next & previous; clamping
	elif action == "seqStepUp":
		UI.seqstep += UI.seqstepsize
		
		if UI.seqstep > UI.seqstepmax - UI.seqstepsize:
			UI.seqstep = 0

	elif action == "seqStepDown":
		UI.seqstep -= UI.seqstepsize

		if UI.seqstep < 0:
			UI.seqstep = UI.seqstepmax - UI.seqstepsize
	

	# Pattern Stepping
	elif action == "patternStepUp":
		UI.gv.patternChange += 1
	elif action == "patternStepDown":
		UI.gv.patternChange -= 1


	# Play / Pause toggle
	elif action == "playPause":
		togglePlayPause()

	return 0

def clampSequencerStep(seqstep):
	# Handles sequencer stepping, also pattern stuff

	# Clamp step to roll back when it gets too high; add 1 to patternStep
	if seqstep > UI.seqstepmax - UI.seqstepsize:
		seqstep = 0

		# If there's a pattern change pending, execute it (because we have rolled back to 0)
		if UI.gv.patternChange != 0:
			changePendingPattern()

		# However, if there's no pattern change pending; just add 1
		else:
			UI.gv.patternStep += 1

	elif seqstep < 0:
		seqstep = UI.seqstepmax - UI.seqstepsize
		UI.gv.patternStep -= 1

	return seqstep

def clampPatternStepping():
	# Clamps pattern step

	if UI.gv.patternStep > UI.patternMax:
		UI.gv.patternStep = 1
	elif UI.gv.patternStep < 1:
		UI.gv.patternStep = UI.patternMax

def clampPendingStepping():
	# Calculate pending pattern stepping. Basically a fancy clamp

	if UI.gv.patternChange != 0:																
		if UI.gv.patternChange > UI.patternMax - UI.gv.patternStep:		
			UI.gv.patternChange -= UI.patternMax													

		if UI.gv.patternChange + UI.gv.patternStep < 1:
			UI.gv.patternChange += UI.patternMax

	UI.gv.patternPending = UI.gv.patternStep + UI.gv.patternChange
	
def changePendingPattern():
	# Applies pending patternStep changes
	UI.gv.patternStep = UI.gv.patternPending
	UI.gv.patternChange = 0
	UI.gv.patternPending = 0

def startSeqTimer():
	# Ticks 
	UI.tic = time.perf_counter()
	return UI.tic

def sequencerTimer():
	# Times the stepping events based on BPM
	if UI.gv.playing:
		if UI.start_timer == True:
			UI.start_timer = False
			startSeqTimer()
		
		# " if current time - last tic time > bpm time" ...
		if time.perf_counter() - UI.tic > ( 60 / UI.gv.bpm / 4):
			UI.seqstep += UI.seqstepsize
			UI.start_timer = True

def togglePlayPause():
	if UI.gv.playing == True:
		UI.gv.playing = False
	else:
		UI.gv.playing = True


## Curses Starting & Resetting 

def doWindowSetup():
	# Initializes curses and the main window

	UI.window = curses.initscr()

	curses.noecho()
	curses.cbreak()
	curses.curs_set(0)
	curses.start_color()
	
	UI.window.clear()            # Clears the screen
	UI.window.nodelay(True)
	UI.window.border()

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
import curses, traceback
from curses.textpad import Textbox, rectangle
from curses import wrapper
import GlobalVars
import time
import math
import config

# TODO: debugging window thingy for putting vars in
# Could make a little command like structure like in vim; show bar on bottom of screen
# and have a key1+key2 for selecting focus of debug output var

class UI:
	bpm = config.sequencer['bpm']
	seqstep = 0																	
	seqstepmax = config.sequencer['seqstepmax']
	seqstepsize = config.sequencer['seqstepsize']
	begin_x = config.sequencer['begin_x'] 
	begin_y = config.sequencer['begin_y']
	height = config.sequencer['height']
	width = config.sequencer['width']
	
	seqwin = None
	window = None
	start_timer = True
	char = None
	tic = None

	app_version = config.general['app_version']
	gv = GlobalVars.GlobalVars()

def main():
	doWindowSetup() # Initial Window Setup

	drawTitle()
	UI.window.addstr(1, 1, " O / P: control seq step ", curses.A_ITALIC)
	UI.window.addstr(2, 1, " K / L: control bpm ", curses.A_ITALIC)

	drawSequencerWindow()
	
def update_ui():
	UI.char = UI.window.getch()	

	if UI.char == ord('q'): 																		# Quit?
		restoreScreen()
		return 1							
	elif UI.char == ord('r') or UI.char == curses.KEY_RESIZE:		# Resize or Reset window?
		#resetScreen()
		return 2	

	UI.bpm = inputBpm(UI.char, UI.bpm)
	UI.seqstep = inputSeq(UI.char, UI.seqstep, UI.seqstepmax)																# Process sequencer stepping input

	
	draw_sequencer(UI.seqwin, UI.seqstep)																											# Draw sequencer
	sequencerTimer() # Manages sequencer timer

	drawInfo()

	UI.window.refresh()
	UI.seqwin.refresh()

	UI.gv.setSeqstep(UI.seqstep)	# Returns new sequencer step to global vars

	return 0

def sequencerTimer():
	if UI.start_timer == True:
		UI.start_timer = False
		UI.tic = startSeqTimer()
	
	if time.perf_counter() - UI.tic > UI.bpm:
		UI.seqstep += UI.seqstepsize
		UI.start_timer = True
		
def doWindowSetup():
	UI.window = curses.initscr()

	curses.noecho()
	curses.cbreak()
	curses.curs_set(0)
	curses.start_color()
	
	UI.window.clear()            # Clears the screen
	UI.window.nodelay(True)
	UI.window.border()

def drawTitle():
	# Function for drawing the window title, figuring out where it's supposed to go

	width = 20
	titleString = "   RPi MIDI Controller / Sequencer {}   ".format(UI.app_version)
	titleLength = len(titleString)
	screenHeight,screenWidth = UI.window.getmaxyx()


	width = math.floor(screenWidth / 2 - titleLength / 2)
	UI.window.addstr(0, width, titleString, curses.A_REVERSE | curses.A_BOLD)

def drawInfo():
	UI.seqwin.addstr(0, 25, " step:    ".format(UI.seqstep), curses.A_ITALIC)									# Fixes a bug in rendering strings
	UI.seqwin.addstr(0, 25, " step: {} ".format(UI.seqstep), curses.A_ITALIC)									# Show seq step
	UI.window.addstr(3, 1, " BPS:    ".format(UI.seqstep), curses.A_ITALIC)										# Fix bug
	UI.window.addstr(3, 1, " BPS: {} ".format(UI.bpm), curses.A_ITALIC | curses.A_DIM)				# Show BPM


#def getInput():
	# Get Window input and process accordingly

def drawSequencerWindow():
	# Sequencer Window
	UI.seqwin = curses.newwin(UI.height, UI.width, UI.begin_y, UI.begin_x)
	UI.seqwin.border()
	UI.seqwin.addstr(0, 2, "   SEQUENCER   ", curses.A_BOLD | curses.A_REVERSE)	# Title
	UI.start_timer = True

def draw_sequencer(seqwin, seqstep):
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

# Handles input for sequencer stepping
def inputSeq(char, seqstep, seqstepmax):
	if char == ord('p'):
		seqstep += UI.seqstepsize
	elif char == ord('o'):
		seqstep -= UI.seqstepsize

	# Clamp step to roll back when it gets too high
	if seqstep > seqstepmax - UI.seqstepsize:
		seqstep = 0

	elif seqstep < 0:
		seqstep = seqstepmax - UI.seqstepsize

	return seqstep

# Handles input for BPM changes
def inputBpm(char, bpm):
	if char == ord('l'):
		bpm -= 0.05
	elif char == ord('k'):
		bpm += 0.05

	if bpm < 0:								# Clamping
		bpm = 0

	bpm = round(bpm, 2)					# Round it to 2 decimals...
	return bpm								# ...and return it

def startSeqTimer():
	UI.tic = time.perf_counter()
	return UI.tic

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
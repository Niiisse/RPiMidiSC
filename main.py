import curses as c, curses
from curses.textpad import Textbox, rectangle
from curses import wrapper
import time
import math

app_version = "v 0.1"

seqstepmax = 64				# Used for total sequencer steps
seqstepsize = 2				# Amount per step

def main(window):
	# SETUP
	window.clear()            # Clears the screen
	window.nodelay(True)
	window.border()
	c.curs_set(0)
	window.addstr(0, 20, "   RPi MIDI Controller / Sequencer {}   ".format(app_version), curses.A_REVERSE | curses.A_BOLD)
	window.addstr(1, 1, " O / P: control seq step ", curses.A_ITALIC)
	window.addstr(2, 1, " K / L: control bpm ", curses.A_ITALIC)

	# MOAR SETUP
	bpm = 0.25 				# TODO: Write function for dynamically setting BPM to BPS

	# Sequencer Window
	begin_x = 23; begin_y = 6
	height = 9; width = 36
	seqwin = curses.newwin(height, width, begin_y, begin_x)
	seqwin.border()
	seqstep = 0
	seqwin.addstr(0, 2, "   SEQUENCER   ", curses.A_BOLD | curses.A_REVERSE)	# Title
	
	start_timer = True

	# UI LOOP
	while (True):
		char = window.getch()																																# Get character
		seqstep = inputSeq(char, seqstep, seqstepmax)																# Process sequencer stepping input
		bpm = inputBpm(char, bpm)
		seqwin.addstr(0, 25, " step:    ".format(seqstep), curses.A_ITALIC)									# Fixes a bug in rendering strings
		seqwin.addstr(0, 25, " step: {} ".format(seqstep), curses.A_ITALIC)									# Show seq step
		window.addstr(3, 1, " BPS:    ".format(seqstep), curses.A_ITALIC)										# Fix bug
		window.addstr(3, 1, " BPS: {} ".format(bpm), curses.A_ITALIC | curses.A_DIM)				# Show BPM
		draw_sequencer(seqwin, seqstep)																											# Draw sequencer



		# Timer
		if start_timer == True:
			start_timer = False
			tic = startSeqTimer()
		
		if time.perf_counter() - tic > bpm:
			seqstep += seqstepsize
			start_timer = True

		window.refresh()
		seqwin.refresh()


# Draws main sequencer
def draw_sequencer(seqwin, seqstep):

	c.init_pair(1, c.COLOR_WHITE, c.COLOR_BLUE)		# Active Seq color pair
	c.init_pair(2, c.COLOR_WHITE, c.COLOR_BLACK)	# Inactive Seq color pair

	for y in range(5):
		for x in range(32):
				draw_x = 2 + x
				draw_y = 2 + y
				drawstep = seqstep

				# Setting Color Logic
				color_pair = c.color_pair(2)

				if seqstep >= 32:																							# Drawstep is used for second row highlighting
					drawstep = seqstep - (seqstepmax/2)

				if seqstep <= 31:																							# First 32 steps = first row	
					if x >= drawstep and x <= drawstep + 1 and y < 2:
						color_pair = c.color_pair(1)

				elif seqstep >= 30:																						# Second 32 steps = second row
					if x >= drawstep and x <= drawstep + 1 and y > 2:						
						color_pair = c.color_pair(1)

				if y != 2:																										# Make sure there's a blank line inbetween
					seqwin.addstr(draw_y, draw_x, "*", color_pair | c.A_BOLD)		# Draw the seq chars

# Handles input for sequencer stepping
def inputSeq(char, seqstep, seqstepmax):
	if char == ord('p'):
		seqstep += seqstepsize
	elif char == ord('o'):
		seqstep -= seqstepsize

	# Clamp step to roll back when it gets too high
	if seqstep > seqstepmax - seqstepsize:
		seqstep = 0

	elif seqstep < 0:
		seqstep = seqstepmax - seqstepsize

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
	tic = time.perf_counter()
	return tic


wrapper(main)
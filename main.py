import curses as c, curses
from curses.textpad import Textbox, rectangle
from curses import wrapper
import time

def draw_sequencer(seqwin, seqstep):
	c.init_pair(1, c.COLOR_WHITE, c.COLOR_BLUE)		# Active Seq color pair
	c.init_pair(2, c.COLOR_WHITE, c.COLOR_BLACK)	# Inactive Seq color pair

	for y in range(5):
		for x in range(32):
				draw_x = 2 + x
				draw_y = 2 + y

				# Set color
				if x >= seqstep and x <= seqstep+1 and y <= 2:
					color_pair = c.color_pair(1)
				else:
					color_pair = c.color_pair(2)
				
				if y != 2:																										# Make sure there's a blank line
							seqwin.addstr(draw_y, draw_x, "*", color_pair | c.A_BOLD)		# Draw the seq chars

def main(window):
	# SETUP

	window.clear()            # Clears the screen
	window.border()
	c.curs_set(0)

	window.addstr(3, 2, "Current mode: BOLD", curses.A_BOLD)
	window.addstr(1, 2, "Current mode: REVERSE", curses.A_REVERSE)
	window.addstr(2, 2, "Current mode: BLINK", curses.A_BLINK)
	window.addstr(4, 2, "Current mode: DIM", curses.A_DIM)
	window.addstr(5, 2, "Current mode: STANDOUT", curses.A_STANDOUT)
	window.addstr(6, 2, "Current mode: UNDERLINE", curses.A_UNDERLINE)	#curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)	

	# Sequencer Window
	begin_x = 25; begin_y = 10
	height = 9; width = 36
	seqwin = curses.newwin(height, width, begin_y, begin_x)
	seqwin.border()

	seqwin.addstr(0, 2, "   SEQUENCER   ", curses.A_BOLD | curses.A_REVERSE)	# Title

	# LOOP
	while (True):
		draw_sequencer(seqwin, 2)		# Draw sequencer

		window.refresh()
		seqwin.refresh()

	val = window.getch()


wrapper(main)
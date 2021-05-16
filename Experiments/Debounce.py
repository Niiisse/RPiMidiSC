import time

# Debouncing class
# Example usage:
#
#			btPlus = not GPIO.input(BT_BPM_PLUS)
#
#  		if btPlus:
#   		bpmPlusDb.setState(btPlus)
#    		if bpmPlusDb.checkDebounce():
#      		bpmUp()
#
#  		elif not btPlus and bpmPlusDb.btDown:
#    		bpmPlusDb.setState(btPlus)
#
#		By Niisse (2021-04-16)

class Debounce:
	def __init__(self):
		self.tic = time.time()						# First time point for comparing (sets after each succesful execution)
		self.toc = 0											#	Second time point for comparing (set when button is pressed)
		self.initialWait = 0.15						# Waiting time in seconds for first debounce (tapping button)
		self.secondWait = 1								#	Waiting time in s after which button will start continuous press
		self.thirdWait = 0.1							# Waiting time between new continuous sends
		self.continuousPress = False			# Flag used for continuous press (keeping button pressed down)
		self.btPreviouslyPressed = False	# Flag whether button was pressed down the previous frame
		self.btDown = False								# Flag for whether the button is pressed down currently
		self.btUp = True									# Flag for whether the button is depressed currently (like me)


	def checkDebounce(self):
		self.toc = time.time()       							# Set current time
		canGo = False                     				# Makes sure there's an output

		if not self.btPreviouslyPressed:						# New press?
			self.btPreviouslyPressed = True						# For keeping track of button events

			if self.toc - self.tic > self.initialWait:    # Check current time against last time
				self.tic = time.time()												# Update tic timer
				canGo = True																	# Signals return

		elif not self.continuousPress:										# First continous press
			if self.toc - self.tic > self.secondWait:					# Have we waited a second?
				self.tic = time.time()													# Set new time to compare against
				self.continuousPress = True											# For keeping track of holding down
				canGo = True																		# Signals return
		
		else:																							# Continuing continuous press
			if self.toc - self.tic > self.thirdWait:					# Compare time
				self.tic = time.time()													# Set new time to compare against
				canGo = True																		# Signals return

		return canGo  															# Signals return

	def setState(self, btState):									# Sets current button state
		if not self.btDown and btState:								# is button down flag not already set, and button is pressed?
			self.btDown = True														# Set flag
			self.btUp = False															# Set flag

		elif self.btDown and not btState:							# Do the same, but for button up
			self.btDown = False														# Set state
			self.btUp = True															# Set state

			self.btPreviouslyPressed = False							# Reset state
			self.continuousPress = False									# Same 'ere
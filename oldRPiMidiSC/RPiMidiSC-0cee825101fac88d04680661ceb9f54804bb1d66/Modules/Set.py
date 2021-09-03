from . import Pattern

class Set:
	def __init__(self, seqStepAmount, patternAmount):
		self.patterns = [Pattern.Pattern(seqStepAmount) for i in range(patternAmount+1)] # List that holds Patterns
		self.bpm = 120


	# TODO: move bpm stuff to here
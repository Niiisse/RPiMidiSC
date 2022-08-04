from . import Pattern


class Set:
	def __init__(self, seqStepAmount, patternAmount):
		self.patterns = [Pattern.Pattern(seqStepAmount) for i in range(patternAmount+1)] # List that holds Patterns
		self.patternAmount = patternAmount
		self.bpm = 120

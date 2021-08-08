# Sometimes... You just gotta save the load, man.
import csv

class SaveLoad:
	""" Handles saving / loading songs
	
	Basically dumps the sequencer into a CSV file, or loads the sequencer with values from one.
	TODO: Save selecting logic """

	def __init(self):
		pass

	def save(self, index: int, sequencer: object) -> None:
		""" Saves sequencer state to CSV """
		
		header = [              # Holds CSV Header Row
			'pattern',
			'step',
			'layer',
			'note',
			'octave',
			'channel',
			'sustain',
			'arm',
			'lastPlayedNote',
			'lastPlayedChannel',
			'selectedLayer0',
			'selectedLayer1',
			'selectedLayer2',
			'selectedLayer3',
			'enabled'
		]     
	
		sequencerData = []            # Will hold sequencer data

		# Loop over all patterns, then all steps, then all note layers. Copy all the relevant data
		# for each step into a list (rowData), then put this row in sequencerData. 
		# Then, write each row to the csv file.

		# Loop de loop
		for i in range(sequencer.patternAmount):
			for o in range(sequencer.sequencerSteps):
				for u in range(sequencer.noteLayerAmount):
					step = sequencer.patterns[i].patternSteps[o]
					layer = sequencer.patterns[i].patternSteps[o].noteLayers[u]
					rowData = [
						i, 
						o,
						u, 
						layer.note, 
						layer.octave, 
						layer.midiChannel, 
						layer.sustain, 
						layer.arm, 
						layer.lastPlayed[0],
						layer.lastPlayed[1],
						step.selectedLayer[0],
						step.selectedLayer[1],
						step.selectedLayer[2],
						step.selectedLayer[3],
						step.enabled
					] 

					sequencerData.append(rowData)

		# Get path string, open file and write data
		path = "songs/" + str(index) + ".csv"

		with open(path, mode='w') as csvFile:

			# Init CSV Writer, write header data then row data
			writer = csv.writer(csvFile)
			writer.writerow(header)
			writer.writerows(sequencerData)

		
	def load(self, index: int, sequencer: object) -> None:
		""" Loads a CSV file, applies contents to Sequencer. """

		path = "songs/" + str(index) + ".csv"

		with open(path, mode='r') as csvFile:
			reader = csv.DictReader(csvFile)
			rowList = list(reader)

			sequencer.seqstep = 0
			sequencer.patternStep = 1
		
		#TODO: get patternAmount

		for row in rowList:
			step = sequencer.patterns[int(row['pattern'])].patternSteps[int(row['step'])]
			layer = sequencer.patterns[int(row['pattern'])].patternSteps[int(row['step'])].noteLayers[int(row['layer'])]
			
			layer.arm = bool(row['arm'])
			layer.channel = int(row['channel'])
			layer.lastNote = (int(row['lastPlayedNote']), int(row['lastPlayedChannel']))
			layer.note = int(row['note'])
			layer.octave = int(row['octave'])
			layer.sustain = bool(row['sustain'])
			step.selectedLayer=[int(row['selectedLayer0']), int(row['selectedLayer1']), int(row['selectedLayer2']), int(row['selectedLayer3'])]
			step.enabled = bool(row['enabled'])


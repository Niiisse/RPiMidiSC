# Sometimes... You just gotta save the load, man.
import csv

class SaveLoad:
	""" Handles saving / loading songs
	
	Dumps the sequencer into a CSV file, or loads the sequencer with values from one.
	TODO: Save-selecting logic 
	TODO: backup file before writing """

	def __init__(self):
		self.folderName = "saves/"				# Name of folder containing saves
		
	def save(self, index: int, sequencer: object) -> None:
		""" Saves sequencer state to CSV """
		
		# Metadata
		metaHeader = [
			'id',
			'bpm',
			'patternAmount',
			'patternMode'
		]

		# Get old data, update relevant rows, then save
		# Normally a list of dicts is returned. We need to convert this  to a list of lists,
		# because we can't re-save the CSV file properly otherwise.

		metaRowList = self.convertMetadataToList(self.readMetadata())
		metaRow = [index, sequencer.bpm, sequencer.patternAmount, sequencer.patternMode]
		metaRowList[index] = metaRow
		
		metaPath = self.folderName + "metadata.csv"
		with open(metaPath, mode='w') as metaFile:

			# Init CSV Writer, write header data then row data
			writer = csv.writer(metaFile)
			writer.writerow(metaHeader)
			writer.writerows(metaRowList)

		# Savedata
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
		for i in range(1, sequencer.patternAmount+1):			# FIXME: this +1 business is no good. should have pattern and patternAmount internally count from 0
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
		path = self.folderName + str(index) + ".csv"

		with open(path, mode='w') as csvFile:

			# Init CSV Writer, write header data then row data
			writer = csv.writer(csvFile)
			writer.writerow(header)
			writer.writerows(sequencerData)
		
	def load(self, index: int, sequencer: object) -> None:
		""" Loads a CSV file, applies contents to Sequencer. """

		metaRowList = self.readMetadata()

		# Get savedata
		path = self.folderName + str(index) + ".csv"

		with open(path, mode='r') as csvFile:
			reader = csv.DictReader(csvFile)
			rowList = list(reader)

		# Re-setup sequencer
		sequencer.seqstep = 0
		sequencer.patternStep = 1
		sequencer.patternAmount = int(metaRowList[index]['patternAmount'])
		sequencer.initPatterns()
		sequencer.patternMode = metaRowList[index]['patternMode']
		sequencer.bpm = int(metaRowList[index]['bpm'])
		
		# Loop over all rows, copy data to sequencer
		for idx, row in enumerate(rowList):
			if idx < sequencer.patternAmount * sequencer.noteLayerAmount * sequencer.sequencerSteps:
				step = sequencer.patterns[int(row['pattern'])].patternSteps[int(row['step'])]
				layer = sequencer.patterns[int(row['pattern'])].patternSteps[int(row['step'])].noteLayers[int(row['layer'])]
				
				layer.arm = bool(row['arm'])
				layer.midiChannel = int(row['channel'])
				layer.lastNote = (int(row['lastPlayedNote']), int(row['lastPlayedChannel']))
				layer.note = int(row['note'])
				layer.octave = int(row['octave'])
				layer.sustain = True if row['sustain'] == 'True' else False		# FIXME: save sustain as 0/1
				step.selectedLayer=[int(row['selectedLayer0']), int(row['selectedLayer1']), int(row['selectedLayer2']), int(row['selectedLayer3'])]
				step.enabled = bool(row['enabled'])		

	def readMetadata(self) -> dict:
		""" Gets metadata from file, returns dict 
		
		Used for loading data """

		# Get metadata
		metaPath = self.folderName + "metadata.csv"
		
		with open(metaPath, mode='r') as metaCsvFile:
			metaReader = csv.DictReader(metaCsvFile)
			return list(metaReader)

	def convertMetadataToList(self, metadata: dict) -> list:
		""" Takes metadata list of dicts and converts it to lists

		Used for re-saving metadata file """

		metaList = []
		for row in metadata:
			metaList.append(list(row.values()))

		return metaList
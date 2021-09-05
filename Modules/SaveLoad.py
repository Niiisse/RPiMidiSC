# Sometimes... You just gotta save the load, man.
import csv

class SaveLoad:
	""" Handles saving / loading songs
	
	Dumps the sequencer into a CSV file, or loads the sequencer with values from one.
	TODO: backup file before writing """

	# FIXME: set integration

	def __init__(self):
		self.folderName = "saves/"				# Name of folder containing saves
		
	def save(self, index: int, sequencer: object) -> None:
		""" Saves sequencer state to CSV 

		Metadata 	- set header
							- convert to list
							- convert index from str to int for comparing
							- remove all old items with current index
							- loop over all sets; add data to list
							- add this list of lists to metadata list
							- sort the metadata list
							- save it
		
		Then, save sequencer's data into a big ol' list. Save this list to correct file.
		TODO: Make backup of old file before writing to it.
		
		"""
		
		# METADATA #

		metaHeader = [
			'id',
			'set',
			'bpm',
			'patternAmount',
			'patternMode',
			'setRepeat'
		]

		# Get old data, update relevant rows, then save
		# Normally a list of dicts is returned. We need to convert this  to a list of lists,
		# because we can't re-save the CSV file properly otherwise.

		metaRowList = self.convertDictToList(self.readMetadata())

		# Change index to int for sorting
		for row in metaRowList:
			row[0] = int(row[0])

		# Remove all lines with current index
		metaRowList = [ elem for elem in metaRowList if elem[0] != index ]
		
		# Create new list of relevant sections
		newMetaRows = []

		# Loop over list; create rows
		for i in range(sequencer.setsAmount+1):
			setRow = [
				index,
				i,
				sequencer.sets[i].bpm, 
				sequencer.sets[i].patternAmount, 
				sequencer.patternMode,
				1 if sequencer.setRepeat else 0
			]

			newMetaRows.append(setRow)

		# Add rows to meta info list
		for setRow in newMetaRows:
			metaRowList.append(setRow)

		# Sort list based on index
		metaRowList.sort(key=lambda x: x[0])
		
		# Save metadata
		metaPath = self.folderName + "metadata.csv"
		with open(metaPath, mode='w') as metaFile:

			# Init CSV Writer, write header data then row data
			writer = csv.writer(metaFile)
			writer.writerow(metaHeader)
			writer.writerows(metaRowList)


		# ACTUAL SAVE DATA #
		header = [              
			'set',
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
		for s in range(sequencer.setsAmount+1):
			for i in range(1, sequencer.patternAmount+1):		
				for o in range(sequencer.sequencerSteps):
					for u in range(sequencer.noteLayerAmount):
						step = sequencer.sets[s].patterns[i].steps[o]
						layer = sequencer.sets[s].patterns[i].steps[o].noteLayers[u]
						rowData = [
							s,
							i, 
							o,
							u, 
							layer.note, 
							layer.octave, 
							layer.midiChannel, 
							1 if layer.sustain else 0, 
							1 if layer.arm else 0, 
							layer.lastPlayed[0],
							layer.lastPlayed[1],
							step.selectedLayer[0],
							step.selectedLayer[1],
							step.selectedLayer[2],
							step.selectedLayer[3],
							1 if step.enabled else 0
						] 

						sequencerData.append(rowData)

		# Get path string, open file and write our data
		path = self.folderName + str(index) + ".csv"

		with open(path, mode='w') as csvFile:

			# Init CSV Writer, write header data then row data
			writer = csv.writer(csvFile)
			writer.writerow(header)
			writer.writerows(sequencerData)
		
	def load(self, index: int, sequencer: object) -> None:
		""" Loads a CSV file, applies contents to Sequencer. 
		
		Load metadata and a big ol' CSV file containing the song's data, then loop over relevant sequencer sections 
		and fill it with the CSV's data. Lastly, save currently loaded save index to lastLoadedSave in data.csv"""

		metaRowDict = (self.readMetadata())

		# Get savedata
		path = self.folderName + str(index) + ".csv" 

		with open(path, mode='r') as csvFile:
			reader = csv.DictReader(csvFile)
			rowList = list(reader)

		# Re-setup sequencer
		sequencer.playing = False
		sequencer.seqstep = 0
		sequencer.setIndex = 0
		sequencer.patternIndex = 1
		sequencer.patternAmount = int(metaRowDict[index]['patternAmount'])
		sequencer.initSets()
		sequencer.patternMode = metaRowDict[0]['patternMode']		# TODO: change 0 to index
		sequencer.setRepeat = bool(int((metaRowDict[0]['setRepeat'])))
		
		# set bpm
		for i in range(sequencer.setsAmount + 1):
			sequencer.sets[i].bpm = int(metaRowDict[i]['bpm'])

		# Loop over all rows, copy data to sequencer, check prevents index out of bounds
		for idx, row in enumerate(rowList):
			if idx < sequencer.setsAmount * sequencer.patternAmount * sequencer.noteLayerAmount * sequencer.sequencerSteps:
				step = sequencer.sets[int(row['set'])].patterns[int(row['pattern'])].steps[int(row['step'])]
				layer = sequencer.sets[int(row['set'])].patterns[int(row['pattern'])].steps[int(row['step'])].noteLayers[int(row['layer'])]

				layer.arm = bool(int(row['arm']))
				layer.midiChannel = int(row['channel'])
				layer.lastNote = (int(row['lastPlayedNote']), int(row['lastPlayedChannel']))
				layer.note = int(row['note'])
				layer.octave = int(row['octave'])
				layer.sustain = bool(int(row['sustain']))
				step.selectedLayer=[int(row['selectedLayer0']), int(row['selectedLayer1']), int(row['selectedLayer2']), int(row['selectedLayer3'])]
				step.enabled = bool(int(row['enabled']))		

		self.saveLastLoadedSaveIndex(index)

	def readLastLoadedSaveIndex(self) -> int:
		""" Gets last used save-index for startup """

		path = self.folderName + "data.csv"

		with open(path, mode='r') as csvFile:
			reader = csv.DictReader(csvFile)
			rowList = list(reader)

		return int(rowList[0]['lastLoadedSave'])

	def saveLastLoadedSaveIndex(self, index: int) -> None:
		""" Saves loaded song index to file """

		header = ['lastLoadedSave']

		rowList = [index, 0]
		
		path = self.folderName + "data.csv"
		with open(path, mode='w') as file:

			# Init CSV Writer, write header data then row data
			writer = csv.writer(file)
			writer.writerow(header)
			writer.writerow(rowList)

	def readMetadata(self) -> dict:
		""" Gets metadata from file, returns dict 
		
		Used for loading data """

		# Get metadata
		metaPath = self.folderName + "metadata.csv"
		
		with open(metaPath, mode='r') as metaCsvFile:
			metaReader = csv.DictReader(metaCsvFile)
			return list(metaReader)

	def convertDictToList(self, metadata: dict) -> list:
		""" Takes CSV list of dicts and converts it to lists

		Used for re-saving metadata file """

		metaList = []
		for row in metadata:
			metaList.append(list(row.values()))

		return metaList
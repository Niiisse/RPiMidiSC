# FIXME: JSON > CSV
# FIXME: notelayer array can yeet off

import csv

class SaveLoad:
	""" Handles saving / loading songs

	Dumps the sequencer into a CSV file, or loads the sequencer with values from one. """

	metaHeader = [
		'id',
		'set',
		'bpm',
		'patternAmount',
		'patternMode',
		'setRepeat'
	]

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

	def __init__(self):
		self.folderName = "Saves/"				# Name of folder containing saves

	def save(self,
		  index: int,
		  setsAmount: int,
		  sets: list,
		  setRepeat: int,
		  patternMode: str,
		  patternAmount: int,
		  noteLayerAmount: int,
		  stepsAmount: int,
		  ) -> None:
		""" Saves sequencer state to CSV

		Parameter 'setRepeat' already should have gotten +1 to prevent loops from overflowing

		Metadata	- set header
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
		# FIXME: change to constant in class

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
		for i in range(setsAmount):
			setRow = [
				index,
				i,
				sets[i].bpm,
				sets[i].patternAmount,
				patternMode,
				1 if setRepeat else 0
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
			writer.writerow(self.metaHeader)
			writer.writerows(metaRowList)


		# ACTUAL SAVE DATA #

		sequencerData = []            # Will hold sequencer data

		# Loop over all sets, then patterns, then all steps, then all note layers. Copy all the relevant data
		# for each step into a list (rowData), then put this row in sequencerData.
		# Then, write each row to the csv file.

		# Loop de loop
		for s in range(setsAmount):
			for i in range(1, patternAmount):
				for o in range(stepsAmount):
					for u in range(noteLayerAmount):
						step = sets[s].patterns[i].steps[o]
						layer = sets[s].patterns[i].steps[o].noteLayers[u]
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

		sequencerDataDict = []            # Will hold sequencer data

		# Loop over all sets, then patterns, then all steps, then all note layers. Copy all the relevant data
		# for each step into a list (rowData), then put this row in sequencerData.
		# Then, write each row to the csv file.

		# Loop de loop
		for s in range(setsAmount):
			for i in range(1, patternAmount+1):
				for o in range(stepsAmount):
					for u in range(noteLayerAmount):
						step = sets[s].patterns[i].steps[o]
						layer = sets[s].patterns[i].steps[o].noteLayers[u]
						rowData = {
							"set": s,
							"pattern": i,
							"step": o,
							"noteLayer": u,
							"note": layer.note,
							"octave": layer.octave,
							"channel":layer.midiChannel,
							"sustain":1 if layer.sustain else 0,
							"arm":1 if layer.arm else 0, # FIXME: obsolete
							"lastNote":layer.lastPlayed[0],
							"lastChannel":layer.lastPlayed[1],
							"selectedLayer":step.selectedLayer[0],
							"enabled": 1 if step.enabled else 0
						}

						sequencerDataDict.append(rowData)

		# Get path string, open file and write our data
		path = self.folderName + str(index) + ".csv"

		with open(path, mode='w') as csvFile:

			# Init CSV Writer, write header data then row data
			writer = csv.writer(csvFile)
			writer.writerow(self.header)
			writer.writerows(sequencerData)

	def readRowData(self, index: int) -> list:
		""" Returns row data of selected save index """

		path = self.folderName + str(index) + ".csv"

		with open(path, mode='r') as csvFile:
			reader = csv.DictReader(csvFile)
			rowList = list(reader)

		return rowList

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

	def readMetadata(self) -> list[dict]:
		""" Gets metadata from file, returns dict

		Used for loading data """

		# Get metadata
		metaPath = self.folderName + "metadata.csv"

		with open(metaPath, mode='r') as metaCsvFile:
			metaReader = csv.DictReader(metaCsvFile)
			return list(metaReader)

	def convertDictToList(self, metadata: list[dict]) -> list:
		""" Takes CSV list of dicts and converts it to lists

		Used for re-saving metadata file """

		metaList = []
		for row in metadata:
			metaList.append(list(row.values()))

		return metaList

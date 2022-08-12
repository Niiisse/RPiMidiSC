from rich.panel import Panel
from rich.layout import Layout
from rich.align import Align
from rich.table import Table
import config

from Sequencing.Sequencer import Sequencer

class NewUi:
    """ User Interface terminal handler """

    def __init__(self):
        self.uiLayout = self.generateUi()
        self.version = config.general['version']

        self.playStatus = Layout()
        self.noteStatus = Layout()

        self.innerLayout = Layout()
        self.innerLayout.split_column(
            Layout(name="top"),
            Layout(name="bottom")
        )
        self.innerLayout["bottom"].size = 3

        self.innerLayout["top"].split_row(
            Layout(name="left"),
            Layout(name="right")
        )

        self.outerPanel = Panel(self.innerLayout, title=f"[bold]RPiMidiSC {self.version}")
        self.outerLayout = Layout(self.outerPanel)

    def generateUi(self) -> Layout:
        """ Generate UI layout """

        return Layout(Panel("init"))

    def updateUi(self, sequencer: Sequencer, outputStr: str) -> Layout:
        """ Update UI layout """
        self.playStatus.update(self.genPlayStatus(sequencer))
        self.noteStatus.update(self.genNoteStatus(sequencer))

        self.innerLayout["bottom"].update(Align.center(Panel(Align.center(self.genOutputString(outputStr)), title="Hardware Output", expand=False)))
        self.innerLayout["left"].update(self.playStatus)
        self.innerLayout["right"].update(self.noteStatus)

        return self.outerLayout

    def genPlayStatus(self, sequencer: Sequencer) -> str:
        """ Generate play-status related strings """
        brk = "\n"

        stp = f"[bright_white] step:    [bright_cyan]{sequencer.seqstep}\n"
        pat = f"[bright_white] pattern: [bright_cyan]{sequencer.patternIndex} [bright_white]/[bright_cyan] {sequencer.patternAmount}\n"
        set = f"[bright_white] set:     [bright_cyan]{sequencer.setIndex} [bright_white]/[bright_cyan] {sequencer.setsAmount}\n"
        sav = f"[bright_white] save:    [bright_cyan]{sequencer.saveIndex} [bright_white]/[bright_cyan] {sequencer.savesTotal}\n"


        playState = "[bright_green]playing" if sequencer.playing else "[white blink]paused[/]"
        ply = f"[bright_white] state:   {playState}\n"
        bpm = f"[bright_white] bpm:     [bright_green]{sequencer.sets[sequencer.setIndex].bpm}\n"

        patternLoop = "[bright_magenta]yes" if sequencer.patternMode == "single" else "[bright_white]no"
        ptl = f"[bright_white] loop pattern: {patternLoop}\n"

        setLoop = "[bright_magenta]yes" if sequencer.setRepeat else "[bright_white]no"
        stl = f"[bright_white] loop set:     {setLoop}\n"

        hardwareOutput = "[bright_green]enabled" if sequencer.hardwareEnabled else "[bright_red]disabled"
        hwo = f"[bright_white] hardware output: {hardwareOutput}\n"

        midiOutput = "[bright_green]enabled" if sequencer.midiEnabled else "[bright_red]disabled"
        mdo = f"[bright_white] midi output:     {midiOutput}\n"
        return stp + pat + set  + sav + brk + ply + bpm + brk + ptl + stl + brk + hwo + mdo

    def genNoteStatus(self, sequencer: Sequencer) -> Table:
        # TODO: famitracker like view, figure it out

        brk = "\n"
        currentStep = sequencer.sets[sequencer.setIndex].patterns[sequencer.patternIndex].steps[sequencer.seqstep]

        # layerTable = Table(title="Layer")
        # layerTable.add_column("note")
        # layerTable.add_column("layer")
        # layerTable.add_column("octave")
        # layerTable.add_column("channel")

        # for i in range(sequencer.noteLayerAmount):
        #     layerTable.add_row(str(currentStep.noteLayers[i].note),
        #                        str(i),
        #                        str(currentStep.noteLayers[i].octave),
        #                        str(currentStep.noteLayers[i].midiChannel))

        noteTable = Table(title="Note Data")

        # noteTable.add_column()

        # for i in range(10):
        #     noteTable.add_column(str(i))

        # note = f"[bright_white] note: [bright_magenta]{currentStep.noteLayers[0].note}"

        return noteTable

    def genOutputString(self, outputStr: str) -> str:
        """ Generate coloring for outputString """
        ops = f"[bright_white]{outputStr}"
        return ops


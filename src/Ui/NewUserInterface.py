from rich.panel import Panel
from rich.layout import Layout
from rich.align import Align
import config

from Sequencing.Sequencer import Sequencer

class NewUi:
    """ User Interface terminal handler """

    def __init__(self):
        self.uiLayout = self.generateUi()
        self.version = config.general['version']

        self.playStatus = Layout()
        self.playStatus.split_column(
            Layout(name="top"),
            Layout(name="bottom")
        )
        self.playStatus["bottom"].size = 3

        self.innerLayout = Layout()
        self.innerLayout.split_row(
            Layout(name="left"),
            Layout(name="right")
        )

        self.outerPanel = Panel(self.innerLayout, title=f"RPiMidiSC {self.version}")
        self.outerLayout = Layout(self.outerPanel)

    def generateUi(self) -> Layout:
        """ Generate UI layout """

        return Layout(Panel("init"))

    def updateUi(self, sequencer: Sequencer, outputStr: str) -> Layout:
        """ Update UI layout """
        self.playStatus["top"].update(self.genPlayStatus(sequencer))
        self.playStatus["bottom"].update(Panel(Align.center(self.genOutputString(outputStr)), title="Hardware Output"))
        self.innerLayout["left"].update(self.playStatus)


        # uiLayout = Layout(
        #     Panel(
        #         Panel(
        #             f"{sequencer.seqstep},{sequencer.patternIndex}")
        #         title=f"RPiMidiSC {self.version}"
        #     )
        # )

        return self.outerLayout

    def genPlayStatus(self, sequencer: Sequencer) -> str:
        """ Generate play-status related strings """
        brk = "\n"

        stp = f"[bright_white]    step: [bright_cyan]{sequencer.seqstep}\n"
        pat = f"[bright_white] pattern: [bright_cyan]{sequencer.patternIndex} [bright_white]/[bright_cyan] {sequencer.patternAmount}\n"
        set = f"[bright_white]     set: [bright_cyan]{sequencer.setIndex} [bright_white]/[bright_cyan] {sequencer.setsAmount}\n"
        sav = f"[bright_white]    save: [bright_cyan]{sequencer.saveIndex} [bright_white]/[bright_cyan] {sequencer.savesTotal}\n"


        playState = "[bright_green]playing" if sequencer.playing else "[white]paused"
        ply = f"[bright_white]   state: {playState}\n\n"
        return brk + stp + pat + set + sav + brk + ply

    def genOutputString(self, outputStr: str) -> str:
        """ Generate coloring for outputString """
        ops = f"[bright_white]{outputStr}"
        return ops


from rich.panel import Panel
from rich.layout import Layout

from Sequencing.Sequencer import Sequencer

class NewUi:
    """ User Interface terminal handler """

    def __init__(self, version: str):
        self.uiLayout = self.generateUi()
        self.version = version

        self.playStatus = Layout()
        self.playStatus.split_row(
            Layout(name="left"),
            Layout(name="right")
        )

        self.innerLayout = Layout()
        self.innerLayout.split_row(
            Layout(name="left"),
            Layout(name="right")
        )

        self.outerPanel = Panel(self.innerLayout, title=f"RPiMidiSC {version}")
        self.outerLayout = Layout(self.outerPanel)

    def generateUi(self) -> Layout:
        """ Generate UI layout """

        return Layout(Panel("init"))

    def updateUi(self, sequencer) -> Layout:
        """ Update UI layout """
        self.playStatus["left"].update(self.genPlayStatus(sequencer))
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
        ply = f"[bright_white]   state: {playState}"
        return brk + stp + pat + set + sav + brk + ply


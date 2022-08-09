from rich.panel import Panel
from rich.layout import Layout

class NewUi:
    """ User Interface terminal handler """

    def __init__(self):
        self.uiLayout = self.generateUi()

    def generateUi(self) -> Layout:
        """ Generate UI layout """

        return Layout(Panel("init"))

    def updateUi(self, sequencer) -> Layout:
        """ Update UI layout """

        return Layout(Panel(f"{sequencer.seqstep},{sequencer.patternIndex}"))



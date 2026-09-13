"""Full PCBGolf import. Unrouted, unqualified source checkpoint."""
from jitx.design import Design
from .Pcbgolf import Main
from .board import BoardPcbgolf, SubstratePcbgolf

class PcbgolfImported(Design):
    circuit = Main()
    board = BoardPcbgolf()
    substrate = SubstratePcbgolf()

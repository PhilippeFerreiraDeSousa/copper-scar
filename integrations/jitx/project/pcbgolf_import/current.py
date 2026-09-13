"""Full PCBGolf import with preserved keepouts; unrouted and unqualified."""
from jitx.design import Design
from .Pcbgolf import Main
from .board import BoardPcbgolf, SubstratePcbgolf

class PcbgolfFull(Design):
    circuit = Main()
    board = BoardPcbgolf()
    substrate = SubstratePcbgolf()

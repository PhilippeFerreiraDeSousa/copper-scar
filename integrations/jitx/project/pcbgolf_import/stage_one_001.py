from jitx.design import Design
from .Pcbgolf import Main
from .board import BoardPcbgolf, SubstratePcbgolf

class StageOne001(Design):
    circuit = Main()
    board = BoardPcbgolf()
    substrate = SubstratePcbgolf()

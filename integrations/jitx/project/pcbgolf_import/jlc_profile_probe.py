from jitx.design import Design
from .Pcbgolf_placement003 import Main
from .stage_one_002 import FeasibilityBoard
from .fabrication import VerifiedJLC04161H1080
class JLCProfileProbe(Design):
    circuit = Main()
    board = FeasibilityBoard()
    substrate = VerifiedJLC04161H1080()

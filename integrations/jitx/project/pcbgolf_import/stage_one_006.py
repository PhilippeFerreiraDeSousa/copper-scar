from jitx.design import Design
from .Pcbgolf import Main
from .stage_one_002 import FeasibilityBoard
from .fabrication import VerifiedJLC04161H1080
class StageOne006(Design):
    circuit = Main()
    board = FeasibilityBoard()
    substrate = VerifiedJLC04161H1080()

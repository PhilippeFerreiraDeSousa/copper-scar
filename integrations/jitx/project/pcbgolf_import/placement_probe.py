from jitx.design import Design
from .Pcbgolf_placement003 import Main
from .stage_one_002 import FeasibilityBoard, MarginSubstrate
class PlacementProbe(Design):
    circuit = Main()
    board = FeasibilityBoard()
    substrate = MarginSubstrate()

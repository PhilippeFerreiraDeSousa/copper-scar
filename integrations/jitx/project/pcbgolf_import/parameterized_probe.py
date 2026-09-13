from jitx.design import Design
from .Pcbgolf_parameterized import Main
from .stage_one_002 import FeasibilityBoard, MarginSubstrate
class ParameterizedProbe(Design):
    circuit = Main()
    board = FeasibilityBoard()
    substrate = MarginSubstrate()

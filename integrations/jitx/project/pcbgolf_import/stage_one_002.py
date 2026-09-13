from jitx.design import Design
from jitx.board import Board
from jitx.shapes.composites import rectangle
from .Pcbgolf import Main
from .board import SubstratePcbgolf, DesignRules
class RoutingMargin(DesignRules):
    # Prior .2mm native route exported as little as .1626mm: test .05mm extra.
    min_copper_copper_space = 0.25
class MarginSubstrate(SubstratePcbgolf):
    constraints = RoutingMargin()
class FeasibilityBoard(Board):
    shape = rectangle(300, 300)
    signal_area = rectangle(300, 300)
class StageOne002(Design):
    circuit = Main()
    board = FeasibilityBoard()
    substrate = MarginSubstrate()

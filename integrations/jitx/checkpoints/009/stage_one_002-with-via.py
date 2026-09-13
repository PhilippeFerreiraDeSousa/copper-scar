from jitx.design import Design
from jitx.board import Board
from jitx.container import inline
from jitx.via import Via, ViaType
from jitx.shapes.composites import rectangle
from .Pcbgolf import Main
from .board import SubstratePcbgolf, DesignRules
class RoutingMargin(DesignRules):
    # Prior .2mm native route exported as little as .1626mm: test .05mm extra.
    min_copper_copper_space = 0.25
class MarginSubstrate(SubstratePcbgolf):
    constraints = RoutingMargin()
    @inline
    class SourceCompliantThroughVia(Via):
        name = "Source compliant through via 0.60-0.30"
        start_layer = 0
        stop_layer = -1
        diameter = 0.60
        hole_diameter = 0.30
        type = ViaType.MechanicalDrill
class FeasibilityBoard(Board):
    shape = rectangle(300, 300)
    signal_area = rectangle(300, 300)
class StageOne002(Design):
    circuit = Main()
    board = FeasibilityBoard()
    substrate = MarginSubstrate()

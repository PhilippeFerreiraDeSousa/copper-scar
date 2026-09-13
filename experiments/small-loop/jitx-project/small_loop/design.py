from jitx.design import Design
from jitx.via import Via, ViaType
from .imports.SmallLoop.SmallLoop import Main
from .imports.SmallLoop.board import BoardSmallLoop, SubstrateSmallLoop, DesignRules
class PreservedRules(DesignRules):
    # Effective original Default class clearance and nominal width. Native rules
    # remain authority for conditional rules, severities, ERC and footprint QA.
    min_copper_width = 0.2
    min_copper_copper_space = 0.2
    min_drill_diameter = 0.3
    min_silkscreen_width = 0.08
    min_silkscreen_text_height = 0.8
class PreservedSubstrate(SubstrateSmallLoop):
    constraints = PreservedRules()
    class ThroughVia(Via):
        name = 'Original Default 0.60 / 0.30 mm'
        start_layer = 0
        stop_layer = -1
        diameter = 0.6
        hole_diameter = 0.3
        type = ViaType.MechanicalDrill
        tented = True
        via_in_pad = False
class SmallLoopInput(Design):
    circuit = Main()
    board = BoardSmallLoop()
    substrate = PreservedSubstrate()

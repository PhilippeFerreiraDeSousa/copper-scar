# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/board.py 
from jitx.board import Board
from jitx.substrate import Substrate, FabricationConstraints
from jitx.stackup import Stackup, Dielectric, Conductor
from jitx.shapes.composites import rectangle


class Copper(Conductor):
    pass

class Core_1(Dielectric):
    dielectric_coefficient = 4.5
    loss_tangent = 0.02

class KicadProjectStackup(Stackup):
    layers = [
        Copper(thickness=0.035, name="F.Cu"),
        Core_1(thickness=1.51, name="dielectric 1"),
        Copper(thickness=0.035, name="B.Cu"),
    ]

class DesignRules(FabricationConstraints):
    min_copper_width = 0.1016
    min_copper_copper_space = 0.2
    min_copper_hole_space = 0.25
    min_copper_edge_space = 0.025
    min_annular_ring = 0.0762
    min_drill_diameter = 0.2
    min_silkscreen_width = 0
    min_pitch_leaded = 0.35
    min_pitch_bga = 0.35
    max_board_width = 457.2
    max_board_height = 609.6
    min_silk_solder_mask_space = 0.15
    min_silkscreen_text_height = 0.8
    solder_mask_registration = 0.15
    min_soldermask_opening = 0.152
    min_soldermask_bridge = 0.102
    min_th_pad_expand_outer = 0.15
    min_hole_to_hole = 0.25
    min_pth_pin_solder_clearance = 3

class BoardPcbgolf(Board):
    shape = rectangle(300, 200)
    signal_area = rectangle(300, 200)

class SubstratePcbgolf(Substrate):
    stackup = KicadProjectStackup()
    constraints = DesignRules()


"""Four nets, eight top-only pads, and an impassable top-layer keepout.

One net stays on the left; three must cross using actual through vias.
No authored routes or via instances are present initially.
"""
from jitx.board import Board
from jitx.circuit import Circuit
from jitx.component import Component
from jitx.design import Design
from jitx.feature import KeepOut, Soldermask
from jitx.landpattern import Landpattern, Pad, PadMapping
from jitx.layerindex import LayerSet
from jitx.net import Port, Net
from jitx.shapes.composites import rectangle
from jitx.stackup import Stackup, Conductor, Dielectric
from jitx.substrate import Substrate, FabricationConstraints
from jitx.symbol import Symbol, Pin, Direction, SymbolMapping
from jitx.via import Via, ViaType


class TestPad(Pad):
    shape = rectangle(1.2, 1.2)
    soldermask = Soldermask(rectangle(1.4, 1.4))


class TestLandpattern(Landpattern):
    p = TestPad().at(0, 0)


class TestSymbol(Symbol):
    p = Pin((0, 0), 1, Direction.Right)


class Terminal(Component):
    reference_designator_prefix = 'TP'
    p = Port()
    landpattern = TestLandpattern()
    symbol = TestSymbol()
    mappings = [PadMapping({p: landpattern.p}), SymbolMapping({p: symbol.p})]


class ProofCircuit(Circuit):
    hold_left = Terminal().at(-12, 10)
    hold_right = Terminal().at(-7, 10)
    a_left = Terminal().at(-8, 6)
    a_right = Terminal().at(8, 6)
    b_left = Terminal().at(-8, 0)
    b_right = Terminal().at(8, 0)
    c_left = Terminal().at(-8, -3)
    c_right = Terminal().at(8, -3)
    nets = [Net([hold_left.p, hold_right.p], name='HOLD'),
            Net([a_left.p, a_right.p], name='CROSS_A'),
            Net([b_left.p, b_right.p], name='CROSS_B'),
            Net([c_left.p, c_right.p], name='CROSS_C')]


class ProofBoard(Board):
    shape = rectangle(32, 28)
    signal_area = rectangle(32, 28)
    barrier = KeepOut(shape=rectangle(2, 28), layers=LayerSet(0), route=True, via=True, pour=True)


class Copper(Conductor):
    pass


class Core(Dielectric):
    dielectric_coefficient = 4.5
    loss_tangent = 0.02


class ProofStackup(Stackup):
    layers = [Copper(thickness=0.035, name='F.Cu'), Core(thickness=1.51),
              Copper(thickness=0.035, name='B.Cu')]


class ProofRules(FabricationConstraints):
    min_copper_width = 0.2
    min_copper_copper_space = 0.25
    min_copper_hole_space = 0.28
    min_copper_edge_space = 0.5
    min_annular_ring = 0.15
    min_drill_diameter = 0.2
    min_silkscreen_width = 0.15
    min_pitch_leaded = 0.35
    min_pitch_bga = 0.35
    max_board_width = 100
    max_board_height = 100
    min_silk_solder_mask_space = 0.15
    min_silkscreen_text_height = 1
    solder_mask_registration = 0.1
    min_soldermask_opening = 0.15
    min_soldermask_bridge = 0.1
    min_th_pad_expand_outer = 0.15
    min_hole_to_hole = 0.25
    min_pth_pin_solder_clearance = 3


class ProofSubstrate(Substrate):
    stackup = ProofStackup()
    constraints = ProofRules()

    class ThroughVia(Via):
        name = 'Proof through via 0.60-0.30'
        start_layer = 0
        stop_layer = -1
        diameter = 0.6
        hole_diameter = 0.3
        type = ViaType.MechanicalDrill
        tented = True
        via_in_pad = False


class BridgeProof(Design):
    circuit = ProofCircuit()
    board = ProofBoard()
    substrate = ProofSubstrate()

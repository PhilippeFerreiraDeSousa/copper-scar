# File Location: .local/small-loop/jitx/small_loop/imports/SmallLoop/symbols/SymbolNFET_DUAL_COMMON_SOURCE_QS5K2.py 
from jitx.symbol import Symbol, Pin, Direction
from jitx.anchor import Anchor
from jitx.shapes.primitive import Polyline, Circle, Text
from jitx.shapes.composites import rectangle
from jitx.transform import Transform


class SymbolNFET_DUAL_COMMON_SOURCE_QS5K2(Symbol):
    pin_name_size = 0
    pad_name_size = 0
    G1 = Pin((-4, 0), 2, Direction.Left)
    S = Pin((4, -4), 2, Direction.Down)
    G2 = Pin((12, 0), 2, Direction.Right)
    D2 = Pin((8, 2), 2, Direction.Up)
    D1 = Pin((0, 2), 2, Direction.Up)
    draws = [
        Polyline(0.1524, [(1.5, -0.5), (2.5, -0.5)]),
        Polyline(0.1524, [(8, 2), (8, 1.5)]),
        Polyline(0.3048, [(-1.4, 0), (-0.7, 0.2)]),
        Polyline(0.1524, [(5.5, 0.6), (5.3, 0.8)]),
        Polyline(0.1524, [(2, 0.6), (2, 1.5)]),
        Polyline(0.1524, [(2.5, 0.6), (2.7, 0.8)]),
        Polyline(0.254, [(10.88, 1.9), (10.88, -2)]),
        Polyline(0.1524, [(0, -1.5), (0, -2)]),
        Polyline(0.1524, [(8.6, 0), (8, 0)]),
        Polyline(0.1524, [(8.6, 0), (8.6, -0.4)]),
        Polyline(0.1524, [(0, 1.5), (2, 1.5)]),
        Polyline(0.3048, [(8.7, -0.2), (9.4, 0)]),
        Polyline(0.254, [(0, -4), (8, -4)]),
        Polyline(0.1524, [(0, 2), (0, 1.5)]),
        Polyline(0.1524, [(-0.6, 0), (0, 0)]),
        Polyline(0.1524, [(2.5, -0.5), (2, 0.6)]),
        Polyline(0.1524, [(-0.6, -0.4), (-1.6, 0)]),
        Polyline(0.254, [(0, -2), (0, -4)]),
        Polyline(0.1524, [(2, -1.5), (0, -1.5)]),
        Transform((9.9, 0)) * rectangle(0.6, 1.4),
        Polyline(0.1524, [(-0.6, 0), (-0.6, -0.4)]),
        Polyline(0.3048, [(-0.7, 0.2), (-0.7, 0)]),
        Polyline(0.1524, [(2, -1.5), (2, 0.6)]),
        Polyline(0.1524, [(-0.6, 0.4), (-0.6, 0)]),
        Polyline(0.1524, [(9.6, -1.5), (8, -1.5)]),
        Polyline(0.1524, [(0, 1.5), (-1.58, 1.5)]),
        Polyline(0.1524, [(8.6, 0.4), (8.6, 0)]),
        Polyline(0.1524, [(6.5, -0.5), (5.5, -0.5)]),
        Polyline(0.1524, [(1.5, 0.6), (1.3, 0.4)]),
        Polyline(0.254, [(-2.88, 1.9), (-2.88, -2)]),
        Polyline(0.1524, [(-3, 0), (-4, 0)]),
        Polyline(0.1524, [(6.5, 0.6), (6, 0.6)]),
        Polyline(0.1524, [(8.7, 0), (9.6, 0)]),
        Polyline(0.1524, [(6.5, 0.6), (6.7, 0.4)]),
        Polyline(0.1524, [(8, -1.5), (8, -2)]),
        Polyline(0.1524, [(6, 0.6), (6, 1.5)]),
        Polyline(0.1524, [(-0.7, 0), (-1.6, 0)]),
        Polyline(0.3048, [(-0.7, 0), (-0.9, 0)]),
        Polyline(0.1524, [(9.6, 0), (8.6, 0.4)]),
        Polyline(0.1524, [(6, 0.6), (6.5, -0.5)]),
        Polyline(0.1524, [(8, 0), (8, -1.5)]),
        Polyline(0.1524, [(2, 0.6), (1.5, -0.5)]),
        Polyline(0.1524, [(2, 0.6), (2.5, 0.6)]),
        Polyline(0.1524, [(6, -1.5), (8, -1.5)]),
        Polyline(0.1524, [(8.6, -0.4), (9.6, 0)]),
        Polyline(0.1524, [(-1.6, 0), (-0.6, 0.4)]),
        Polyline(0.1524, [(5.5, -0.5), (6, 0.6)]),
        Polyline(0.1524, [(6, -1.5), (6, 0.6)]),
        Polyline(0.1524, [(8, 1.5), (9.58, 1.5)]),
        Polyline(0.1524, [(8, 1.5), (6, 1.5)]),
        Polyline(0.1524, [(-1.6, -1.5), (0, -1.5)]),
        Polyline(0.254, [(8, -4), (8, -2)]),
        Polyline(0.3048, [(8.7, 0.2), (8.7, 0)]),
        Polyline(0.3048, [(9.4, 0), (8.7, 0.2)]),
        Polyline(0.1524, [(1.5, 0.6), (2, 0.6)]),
        Polyline(0.1524, [(0, 0), (0, -1.5)]),
        Transform((-1.9, 0)) * rectangle(0.6, 1.4),
        Transform((9.9, -1.5)) * rectangle(0.6, 1),
        Transform((9.9, 1.5)) * rectangle(0.6, 1),
        Transform((-1.9, 1.5)) * rectangle(0.6, 1),
        Transform((-1.9, -1.5)) * rectangle(0.6, 1),
        Circle(radius=0.1).at(0, -1.5),
        Circle(radius=0.1).at(8, 1.5),
        Circle(radius=0.1).at(0, 1.5),
        Circle(radius=0.1).at(8, -1.5),
        Polyline(0.1524, [(6, 0.6), (5.5, 0.6)]),
        Polyline(0.3048, [(-0.7, -0.2), (-1.4, 0)]),
        Polyline(0.3048, [(8.7, 0), (8.9, 0)]),
        Polyline(0.1524, [(11, 0), (12, 0)]),
        Text("S", 0.54394, Anchor.W).at((-1, -2.8)),
        Text("D", 0.54394, Anchor.E).at((9, 2)),
        Text("D", 0.54394, Anchor.W).at((-1, 2)),
        Text("G", 0.54394, Anchor.W).at((-4, -1)),
        Text("G", 0.54394, Anchor.E).at((12, -1)),
        Text("S", 0.54394, Anchor.E).at((9, -2.8)),
    ]


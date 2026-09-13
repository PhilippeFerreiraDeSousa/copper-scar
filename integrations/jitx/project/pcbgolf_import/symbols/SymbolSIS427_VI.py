# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/symbols/SymbolSIS427_VI.py 
from jitx.symbol import Symbol, Pin, Direction
from jitx.anchor import Anchor
from jitx.shapes.primitive import Polyline, Circle, Text
from jitx.shapes.composites import rectangle
from jitx.transform import Transform


class SymbolSIS427_VI(Symbol):
    pin_name_size = 0
    pad_name_size = 0
    S = Pin((0, -2), 2, Direction.Down)
    G = Pin((-4, 0), 2, Direction.Left)
    D = Pin((0, 2), 2, Direction.Up)
    draws = [
        Polyline(0.3048, [(-0.2, 0), (-0.9, 0.2)]),
        Transform((-1.9, 0)) * rectangle(0.6, 1.4),
        Transform((-1.9, 1.5)) * rectangle(0.6, 1),
        Polyline(0.1524, [(0, -1.5), (0, -2)]),
        Polyline(0.1524, [(1.5, -0.6), (1.3, -0.8)]),
        Polyline(0.3048, [(-0.9, 0), (-0.7, 0)]),
        Polyline(0.1524, [(0, 0), (-1, 0.4)]),
        Polyline(0.1524, [(-1, -0.4), (0, 0)]),
        Polyline(0.1524, [(2, -0.6), (2, 1.5)]),
        Polyline(0.3048, [(-0.9, -0.2), (-0.2, 0)]),
        Polyline(0.1524, [(2.5, 0.5), (1.5, 0.5)]),
        Polyline(0.1524, [(-1.6, -1.5), (0, -1.5)]),
        Polyline(0.1524, [(1.5, 0.5), (2, -0.6)]),
        Polyline(0.1524, [(2.5, -0.6), (2, -0.6)]),
        Polyline(0.1524, [(-3, 0), (-4, 0)]),
        Polyline(0.1524, [(0, 0), (0, -1.5)]),
        Polyline(0.254, [(-2.88, 1.9), (-2.88, -2)]),
        Polyline(0.1524, [(2, -1.5), (2, -0.6)]),
        Polyline(0.3048, [(-0.9, 0.2), (-0.9, 0)]),
        Polyline(0.1524, [(0, 1.5), (-1.58, 1.5)]),
        Transform((-1.9, -1.5)) * rectangle(0.6, 1),
        Circle(radius=0.1).at(0, -1.5),
        Polyline(0.1524, [(0, 2), (0, 1.5)]),
        Circle(radius=0.1).at(0, 1.5),
        Polyline(0.1524, [(2.5, -0.6), (2.7, -0.4)]),
        Polyline(0.1524, [(2, -0.6), (2.5, 0.5)]),
        Polyline(0.1524, [(-1, 0.4), (-1, -0.4)]),
        Polyline(0.1524, [(0, 1.5), (2, 1.5)]),
        Polyline(0.1524, [(2, -0.6), (1.5, -0.6)]),
        Polyline(0.1524, [(-0.9, 0), (-1.6, 0)]),
        Polyline(0.1524, [(2, -1.5), (0, -1.5)]),
        Text("S", 0.54394, Anchor.W).at((-1, -2.8)),
        Text("G", 0.54394, Anchor.W).at((-4, -1)),
        Text("D", 0.54394, Anchor.W).at((-1, 2)),
    ]


# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/symbols/SymbolLED_TH.py 
from jitx.symbol import Symbol, Pin, Direction
from jitx.shapes.primitive import Polyline, Polygon


class SymbolLED_TH(Symbol):
    pin_name_size = 0
    pad_name_size = 0
    A = Pin((0, 0), 2, Direction.Up)
    C = Pin((0, -2), 2, Direction.Down)
    draws = [
        Polyline(0.254, [(1, 0), (-1, 0)]),
        Polyline(0.254, [(1, 0), (0, -2)]),
        Polyline(0.254, [(0, -2), (-1, -2)]),
        Polyline(0.254, [(0, -2), (-1, 0)]),
        Polyline(0.1524, [(-1.5, -1.5), (-2.6, -2.6)]),
        Polyline(0.1524, [(-1.6, -0.6), (-2.7, -1.7)]),
        Polygon([
            (-2.7, -1.7),
            (-2.4, -1),
            (-2, -1.4),
            (-2.7, -1.7)]),
        Polygon([
            (-2.6, -2.6),
            (-2.3, -1.9),
            (-1.9, -2.3),
            (-2.6, -2.6)]),
        Polyline(0.254, [(1, -2), (0, -2)]),
    ]


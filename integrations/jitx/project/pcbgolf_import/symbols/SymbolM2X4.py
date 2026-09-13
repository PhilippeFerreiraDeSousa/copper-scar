# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/symbols/SymbolM2X4.py 
from jitx.symbol import Symbol, Pin, Direction
from jitx.shapes.primitive import Polyline


class SymbolM2X4(Symbol):
    pin_name_size = 0
    pad_name_size = 1.2
    p = {
        1: Pin((-2, 8), 4, Direction.Left),
        2: Pin((2, 8), 4, Direction.Right),
        3: Pin((-2, 6), 4, Direction.Left),
        4: Pin((2, 6), 4, Direction.Right),
        5: Pin((-2, 4), 4, Direction.Left),
        6: Pin((2, 4), 4, Direction.Right),
        7: Pin((-2, 2), 4, Direction.Left),
        8: Pin((2, 2), 4, Direction.Right),
    }
    draws = [
        Polyline(0.6096, [(1, 2), (2, 2)]),
        Polyline(0.4064, [(3, 0), (-3, 0)]),
        Polyline(0.6096, [(1, 4), (2, 4)]),
        Polyline(0.6096, [(1, 6), (2, 6)]),
        Polyline(0.6096, [(1, 8), (2, 8)]),
        Polyline(0.6096, [(-1, 2), (-2, 2)]),
        Polyline(0.6096, [(-1, 4), (-2, 4)]),
        Polyline(0.6096, [(-1, 6), (-2, 6)]),
        Polyline(0.4064, [(3, 0), (3, 10)]),
        Polyline(0.4064, [(-3, 10), (-3, 0)]),
        Polyline(0.4064, [(-3, 10), (3, 10)]),
        Polyline(0.6096, [(-1, 8), (-2, 8)]),
    ]


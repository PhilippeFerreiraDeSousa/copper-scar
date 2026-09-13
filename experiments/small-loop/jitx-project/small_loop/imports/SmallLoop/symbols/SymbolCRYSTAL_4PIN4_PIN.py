# File Location: .local/small-loop/jitx/small_loop/imports/SmallLoop/symbols/SymbolCRYSTAL_4PIN4_PIN.py 
from jitx.symbol import Symbol, Pin, Direction
from jitx.anchor import Anchor
from jitx.shapes.primitive import Polyline, Text


class SymbolCRYSTAL_4PIN4_PIN(Symbol):
    pad_name_size = 0
    p = {
        1: Pin((-2, 0), 0, Direction.Left, pad_name_size=0),
        2: Pin((2, 0), 0, Direction.Right, pad_name_size=0),
        3: Pin((0, 0), 4, Direction.Down, pad_name_size=1.2),
    }
    draws = [
        Polyline(0.1524, [(0.8, 0), (2, 0)]),
        Polyline(0.254, [(-0.8, 1.4), (-0.8, -1.4)]),
        Polyline(0.254, [(0.8, 1.4), (0.8, -1.4)]),
        Polyline(0.254, [(0.3, -1.2), (0.3, 1.2)]),
        Polyline(0.254, [(0.3, 1.2), (-0.3, 1.2)]),
        Polyline(0.254, [(-0.3, -1.2), (0.3, -1.2)]),
        Polyline(0.254, [(-0.3, 1.2), (-0.3, -1.2)]),
        Polyline(0.1524, [(-2, 0), (-0.8, 0)]),
        Text("1", 0.57795, Anchor.W).at((-1.7, -0.9)),
        Text("2", 0.57795, Anchor.W).at((1.2, -0.9)),
    ]


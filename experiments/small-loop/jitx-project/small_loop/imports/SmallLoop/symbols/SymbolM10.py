# File Location: .local/small-loop/jitx/small_loop/imports/SmallLoop/symbols/SymbolM10.py 
from jitx.symbol import Symbol, Pin, Direction
from jitx.shapes.primitive import Polyline


class SymbolM10(Symbol):
    pin_name_size = 1.2
    pad_name_size = 1.2
    p = {
        1: Pin((-4, 10), 4, Direction.Left),
        2: Pin((-4, 8), 4, Direction.Left),
        3: Pin((-4, 6), 4, Direction.Left),
        4: Pin((-4, 4), 4, Direction.Left),
        5: Pin((-4, 2), 4, Direction.Left),
        6: Pin((-4, 0), 4, Direction.Left),
        7: Pin((-4, -2), 4, Direction.Left),
        8: Pin((-4, -4), 4, Direction.Left),
        9: Pin((-4, -6), 4, Direction.Left),
        10: Pin((-4, -8), 4, Direction.Left),
    }
    draws = [
        Polyline(0.6096, [(-4, -10), (-4, 12)]),
        Polyline(0.6096, [(2, 12), (2, -10)]),
        Polyline(0.6096, [(-4, 12), (2, 12)]),
        Polyline(0.6096, [(2, -10), (-4, -10)]),
    ]


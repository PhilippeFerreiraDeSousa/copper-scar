# File Location: .local/small-loop/jitx/small_loop/imports/SmallLoop/symbols/SymbolCREE_RGB_CLMVC.py 
from jitx.symbol import Symbol, Pin, Direction
from jitx.shapes.primitive import Polyline


class SymbolCREE_RGB_CLMVC(Symbol):
    pin_name_size = 1.2
    pad_name_size = 1.2
    COMp = Pin((-8, -4), 4, Direction.Left)
    Rn = Pin((-8, 4), 4, Direction.Left)
    Gn = Pin((6, 4), 4, Direction.Right)
    Bn = Pin((6, -4), 4, Direction.Right)
    draws = [
        Polyline(0.254, [(-8, -8), (6, -8)]),
        Polyline(0.254, [(6, 8), (-8, 8)]),
        Polyline(0.254, [(-8, 8), (-8, -8)]),
        Polyline(0.254, [(6, -8), (6, 8)]),
    ]


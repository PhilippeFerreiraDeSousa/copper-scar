# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/symbols/SymbolVBUS.py 
from jitx.symbol import Symbol, Pin, Direction
from jitx.shapes.primitive import Polyline


class SymbolVBUS(Symbol):
    pin_name_size = 1
    pad_name_size = 1
    p = Pin((0, 0), 0, Direction.Down)
    draws = [
        Polyline(0.127, [(-0.6, 1), (0, 2)]),
        Polyline(0.127, [(0, 2), (0.6, 1)]),
        Polyline(0.127, [(0, 0), (0, 2)]),
    ]


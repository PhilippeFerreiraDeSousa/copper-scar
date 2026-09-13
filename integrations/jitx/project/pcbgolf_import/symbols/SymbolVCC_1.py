# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/symbols/SymbolVCC_1.py 
from jitx.symbol import Symbol, Pin, Direction
from jitx.shapes.primitive import Polyline


class SymbolVCC_1(Symbol):
    pin_name_size = 0
    pad_name_size = 0
    VCC_1 = Pin((0, 2), 2, Direction.Down)
    draws = [
        Polyline(0.254, [(0.6, 1), (0, 2)]),
        Polyline(0.254, [(0, 2), (-0.6, 1)]),
    ]


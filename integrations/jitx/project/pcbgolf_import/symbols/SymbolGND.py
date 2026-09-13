# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/symbols/SymbolGND.py 
from jitx.symbol import Symbol, Pin, Direction
from jitx.shapes.primitive import Polyline


class SymbolGND(Symbol):
    pin_name_size = 0
    pad_name_size = 0
    GND = Pin((0, 0), 2, Direction.Up)
    draw = Polyline(0.254, [(-1.5, 0), (1.5, 0)])


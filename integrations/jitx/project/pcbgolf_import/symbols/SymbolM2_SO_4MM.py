# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/symbols/SymbolM2_SO_4MM.py 
from jitx.symbol import Symbol, Pin, Direction
from jitx.shapes.primitive import Circle


class SymbolM2_SO_4MM(Symbol):
    pin_name_size = 0
    pad_name_size = 0
    p = {
        1: Pin((-2, 0), 2, Direction.Left),
    }
    draw = Circle(radius=2)


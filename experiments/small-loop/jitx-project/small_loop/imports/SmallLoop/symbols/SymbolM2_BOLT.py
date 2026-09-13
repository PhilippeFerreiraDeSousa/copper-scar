# File Location: .local/small-loop/jitx/small_loop/imports/SmallLoop/symbols/SymbolM2_BOLT.py 
from jitx.symbol import Symbol, Pin, Direction
from jitx.shapes.primitive import Circle


class SymbolM2_BOLT(Symbol):
    pin_name_size = 0
    pad_name_size = 0
    p = {
        1: Pin((-2, 0), 2, Direction.Left),
    }
    draw = Circle(radius=2)


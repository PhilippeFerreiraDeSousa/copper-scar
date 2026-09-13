# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/symbols/SymbolNCS20071XV_1.py 
from jitx.symbol import Symbol, Pin, Direction
from jitx.shapes.primitive import Polygon


class SymbolNCS20071XV(Symbol):
    pin_name_size = 1
    pad_name_size = 1
    p = {
        0: Pin((-4, 2), 2, Direction.Left),
        1: Pin((4, 0), 2, Direction.Right),
    }
    Vn = Pin((-2, -3), 3, Direction.Down)
    n = Pin((-4, -2), 2, Direction.Left)
    Vp = Pin((-2, 3), 3, Direction.Up)
    draw = Polygon([
        (4, 0),
        (-4, 4),
        (-4, -4),
        (4, 0)])


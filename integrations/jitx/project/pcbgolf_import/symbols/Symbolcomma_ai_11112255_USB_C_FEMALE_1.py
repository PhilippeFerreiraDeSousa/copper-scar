# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/symbols/Symbolcomma_ai_11112255_USB_C_FEMALE_1.py 
from jitx.symbol import Symbol, Pin, Direction
from jitx.anchor import Anchor
from jitx.shapes.primitive import Polyline, Text


class Symbolcomma_ai_11112255_USB_C_FEMALE(Symbol):
    pin_name_size = 1.2
    VBUS = {
        0: Pin((-10, 12), 4, Direction.Left, pin_name_size=1.2),
        1: Pin((-10, 10), 4, Direction.Left, pin_name_size=1.2),
        2: Pin((10, 12), 4, Direction.Right, pin_name_size=0),
        3: Pin((10, 10), 4, Direction.Right, pin_name_size=0),
    }
    GND = {
        0: Pin((-10, -8), 4, Direction.Left, pin_name_size=1.2),
        1: Pin((-10, -10), 4, Direction.Left, pin_name_size=1.2),
        2: Pin((10, -8), 4, Direction.Right, pin_name_size=0),
        3: Pin((10, -10), 4, Direction.Right, pin_name_size=0),
    }
    TX1p = Pin((-10, 6), 4, Direction.Left, pin_name_size=1.2)
    TX1n = Pin((-10, 4), 4, Direction.Left, pin_name_size=1.2)
    CC1 = Pin((-10, 8), 4, Direction.Left, pin_name_size=1.2)
    DA = Pin((-10, -2), 4, Direction.Left, pin_name_size=1.2)
    D_A = Pin((-10, -4), 4, Direction.Left, pin_name_size=1.2)
    SBU1 = Pin((-10, -6), 4, Direction.Left, pin_name_size=1.2)
    RX2n = Pin((-10, 0), 4, Direction.Left, pin_name_size=1.2)
    RX2p = Pin((-10, 2), 4, Direction.Left, pin_name_size=1.2)
    TX2p = Pin((10, 2), 4, Direction.Right, pin_name_size=0)
    TX2n = Pin((10, 0), 4, Direction.Right, pin_name_size=0)
    CC2 = Pin((10, 8), 4, Direction.Right, pin_name_size=0)
    DB = Pin((10, -4), 4, Direction.Right, pin_name_size=0)
    D_B = Pin((10, -2), 4, Direction.Right, pin_name_size=0)
    SBU2 = Pin((10, -6), 4, Direction.Right, pin_name_size=0)
    RX1n = Pin((10, 4), 4, Direction.Right, pin_name_size=0)
    RX1p = Pin((10, 6), 4, Direction.Right, pin_name_size=0)
    SHIELDA = Pin((-10, -12), 4, Direction.Left, pin_name_size=0)
    SHIELDB = Pin((10, -12), 4, Direction.Right, pin_name_size=0)
    draws = [
        Polyline(0.254, [(10, 16), (-10, 16)]),
        Polyline(0.254, [(10, -14), (10, 16)]),
        Polyline(0.254, [(-10, -14), (10, -14)]),
        Polyline(0.254, [(-10, 16), (-10, -14)]),
        Text("USB-C", 1.19, Anchor.W).at((-2.6, 14.2)),
    ]


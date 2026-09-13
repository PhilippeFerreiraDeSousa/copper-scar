# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/components/UNKNOWN/Comp_10132328_10011LF.py 
# To import this component:
#     from .components.UNKNOWN import Comp_10132328_10011LF
#     u1 = Comp_10132328_10011LF.Comp_10132328_10011LF()
from jitx.landpattern import Landpattern, Pad
from jitx.model3d import Model3D
from jitx.symbol import Symbol, Pin, Direction
from jitx.component import Component
from jitx.net import Port
from jitx.landpattern import PadMapping
from jitx.symbol import SymbolMapping
from jitx.feature import Custom, Paste, Cutout, Soldermask, Courtyard
from jitx.layerindex import Side
from jitx.anchor import Anchor
from jitx.shapes.primitive import Polyline, Circle, Polygon, Text
from jitx.shapes.composites import rectangle
from jitx.transform import Transform

import jitx
from shapely.geometry import JOIN_STYLE
from jitx.layerindex import Side
def make_mask_expansion(
    pad_shape,
    layer_func,
    amount: float | None,
    thruhole: bool
):
    if amount is None:
        amount = jitx.current.substrate.constraints.solder_mask_registration if layer_func is Soldermask \
            else 0.0  # default Paste Mask expansion amount
    mask_shape = pad_shape.to_shapely().buffer(amount, join_style=JOIN_STYLE.mitre)
    if mask_shape.is_empty:
        return []
    layers = [layer_func(mask_shape)]
    if thruhole:
        layers.append(layer_func(mask_shape, side=Side.Bottom))
    return layers

def make_soldermask (
    pad_shape,
    *,
    amount: float | None = None,
    thruhole: bool = False):
    return make_mask_expansion(pad_shape, Soldermask, amount, thruhole)

def make_pastemask (
    pad_shape,
    *,
    amount: float | None = None,
    thruhole: bool = False):
    return make_mask_expansion(pad_shape, Paste, amount, thruhole)


class CircleThPad(Pad):
    shape = Circle(radius=0.55)
    cutout = [
        Cutout(Circle(radius=0.35)),
    ]
    soldermask = [
        Soldermask(Circle(radius=0.55)),
        Soldermask(Circle(radius=0.55), side=Side.Bottom),
    ]
    def __init__(self):
        self.solder = make_soldermask(self.shape, amount=0.0508, thruhole=True)

class RectSmdPad_1(Pad):
    shape = rectangle(0.3, 0.88)
    paste = [
        Paste(rectangle(0.3, 0.88)),
    ]
    soldermask = [
        Soldermask(rectangle(0.3, 0.88)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class RectSmdPad_2(Pad):
    shape = rectangle(1.03, 0.5)
    paste = [
        Paste(rectangle(1.03, 0.5)),
    ]
    soldermask = [
        Soldermask(rectangle(1.03, 0.5)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class LandpatternUSB_C_FEMALE_VERT_GCT(Landpattern):
    A1 = RectSmdPad_1().at((-2.75, 0.83))
    A10 = RectSmdPad_1().at((1.75, 0.83))
    A11 = RectSmdPad_1().at((2.25, 0.83))
    A12 = RectSmdPad_1().at((2.75, 0.83))
    A2 = RectSmdPad_1().at((-2.25, 0.83))
    A3 = RectSmdPad_1().at((-1.75, 0.83))
    A4 = RectSmdPad_1().at((-1.25, 0.83))
    A5 = RectSmdPad_1().at((-0.75, 0.83))
    A6 = RectSmdPad_1().at((-0.25, 0.83))
    A7 = RectSmdPad_1().at((0.25, 0.83))
    A8 = RectSmdPad_1().at((0.75, 0.83))
    A9 = RectSmdPad_1().at((1.25, 0.83))
    B1 = RectSmdPad_1().at((2.75, -0.83))
    B10 = RectSmdPad_1().at((-1.75, -0.83))
    B11 = RectSmdPad_1().at((-2.25, -0.83))
    B12 = RectSmdPad_1().at((-2.75, -0.83))
    B2 = RectSmdPad_1().at((2.25, -0.83))
    B3 = RectSmdPad_1().at((1.75, -0.83))
    B4 = RectSmdPad_1().at((1.25, -0.83))
    B5 = RectSmdPad_1().at((0.75, -0.83))
    B6 = RectSmdPad_1().at((0.25, -0.83))
    B7 = RectSmdPad_1().at((-0.25, -0.83))
    B8 = RectSmdPad_1().at((-0.75, -0.83))
    B9 = RectSmdPad_1().at((-1.25, -0.83))
    S1 = CircleThPad().at((-2.4, 2.15))
    S11 = RectSmdPad_2().at(Transform((-3.75, 1), 39))
    S12 = RectSmdPad_2().at(Transform((3.75, 1), 321))
    S13 = RectSmdPad_2().at(Transform((3.75, -1), 39))
    S14 = RectSmdPad_2().at(Transform((-3.75, -1), 321))
    S2 = CircleThPad().at((2.4, 2.15))
    S3 = CircleThPad().at((2.4, -2.15))
    S4 = CircleThPad().at((-2.4, -2.15))

    customlayer = [
        Custom(Polyline(0.1524, [(-4.25, 1.35), (4.25, 1.35)]), name="Fab"),
        Custom(Polyline(0.1524, [(-4.25, -1.35), (-4.25, 1.35)]), name="Fab"),
        Custom(Polyline(0.1524, [(4.25, 1.35), (4.25, -1.35)]), name="Fab"),
        Custom(Polyline(0.1524, [(4.25, -1.35), (-4.25, -1.35)]), name="Fab"),
    ]
    cutout = [
        Cutout(Circle(radius=0.33).at(-3.75, 0)),
        Cutout(Circle(radius=0.33).at(3.75, 0)),
    ]
    soldermask = [
        Soldermask(Circle(radius=0.33).at(-3.75, 0)),
        Soldermask(Circle(radius=0.33).at(-3.75, 0), side=Side.Bottom),
        Soldermask(Circle(radius=0.33).at(3.75, 0)),
        Soldermask(Circle(radius=0.33).at(3.75, 0), side=Side.Bottom),
    ]
    courtyard = [
        Courtyard(Polygon([
            (-0.8, 1.8),
            (0.8, 1.8),
            (0.8, 2.5),
            (-0.8, 2.5)])),
        Courtyard(Polygon([
            (-0.8, -2.5),
            (0.8, -2.5),
            (0.8, -1.8),
            (-0.8, -1.8)])),
    ]

    models = [
        Model3D("10132328-10011LF.step",
            position=(0, 0, 0),
            scale=(1, 1, 1),
            rotation=(0, 0, 0),
        ),
    ]

class Symbolcomma_ai_11112255_USB_C_FEMALEGCT(Symbol):
    pin_name_size = 1.2
    pad_name_size = 1.2
    VBUS = {
        0: Pin((-10, 12), 4, Direction.Left),
        1: Pin((-10, 10), 4, Direction.Left),
        2: Pin((10, 12), 4, Direction.Right),
        3: Pin((10, 10), 4, Direction.Right),
    }
    GND = {
        0: Pin((-10, -8), 4, Direction.Left),
        1: Pin((-10, -10), 4, Direction.Left),
        2: Pin((10, -8), 4, Direction.Right),
        3: Pin((10, -10), 4, Direction.Right),
    }
    TX1p = Pin((-10, 6), 4, Direction.Left)
    TX1n = Pin((-10, 4), 4, Direction.Left)
    CC1 = Pin((-10, 8), 4, Direction.Left)
    DA = Pin((-10, -2), 4, Direction.Left)
    D_A = Pin((-10, -4), 4, Direction.Left)
    SBU1 = Pin((-10, -6), 4, Direction.Left)
    RX2n = Pin((-10, 0), 4, Direction.Left)
    RX2p = Pin((-10, 2), 4, Direction.Left)
    TX2p = Pin((10, 2), 4, Direction.Right)
    TX2n = Pin((10, 0), 4, Direction.Right)
    CC2 = Pin((10, 8), 4, Direction.Right)
    DB = Pin((10, -4), 4, Direction.Right)
    D_B = Pin((10, -2), 4, Direction.Right)
    SBU2 = Pin((10, -6), 4, Direction.Right)
    RX1n = Pin((10, 4), 4, Direction.Right)
    RX1p = Pin((10, 6), 4, Direction.Right)
    SHIELDA = Pin((-10, -12), 4, Direction.Left, pin_name_size=0)
    SHIELDB = Pin((10, -12), 4, Direction.Right, pin_name_size=0)
    draws = [
        Polyline(0.254, [(10, 16), (-10, 16)]),
        Polyline(0.254, [(10, -14), (10, 16)]),
        Polyline(0.254, [(-10, -14), (10, -14)]),
        Polyline(0.254, [(-10, 16), (-10, -14)]),
        Text("USB-C", 1.19, Anchor.W).at((-2.6, 14.2)),
    ]

class Comp_10132328_10011LF(Component):
    description = ""
    mpn = "10132328-10011LF"
    datasheet = ""
    reference_designator_prefix = "J"
    landpattern = LandpatternUSB_C_FEMALE_VERT_GCT()
    VBUS = {
        0: Port(),
        1: Port(),
        2: Port(),
        3: Port(),
    }
    GND = {
        0: Port(),
        1: Port(),
        2: Port(),
        3: Port(),
    }
    TX1p = Port()
    TX1n = Port()
    CC1 = Port()
    DA = Port()
    D_A = Port()
    SBU1 = Port()
    RX2n = Port()
    RX2p = Port()
    TX2p = Port()
    TX2n = Port()
    CC2 = Port()
    DB = Port()
    D_B = Port()
    SBU2 = Port()
    RX1n = Port()
    RX1p = Port()
    SHIELDA = Port()
    SHIELDB = Port()
    symbol = Symbolcomma_ai_11112255_USB_C_FEMALEGCT()
    mappings = [
        SymbolMapping({
            GND[0]: symbol.GND[0], 
            TX1p: symbol.TX1p, 
            TX1n: symbol.TX1n, 
            VBUS[0]: symbol.VBUS[0], 
            CC1: symbol.CC1, 
            DA: symbol.DA, 
            D_A: symbol.D_A, 
            SBU1: symbol.SBU1, 
            VBUS[1]: symbol.VBUS[1], 
            RX2n: symbol.RX2n, 
            RX2p: symbol.RX2p, 
            GND[1]: symbol.GND[1], 
            GND[2]: symbol.GND[2], 
            TX2p: symbol.TX2p, 
            TX2n: symbol.TX2n, 
            VBUS[2]: symbol.VBUS[2], 
            CC2: symbol.CC2, 
            DB: symbol.DB, 
            D_B: symbol.D_B, 
            SBU2: symbol.SBU2, 
            VBUS[3]: symbol.VBUS[3], 
            RX1n: symbol.RX1n, 
            RX1p: symbol.RX1p, 
            GND[3]: symbol.GND[3], 
            SHIELDA: symbol.SHIELDA, 
            SHIELDB: symbol.SHIELDB
        }),
        PadMapping({
            GND[0]: landpattern.A1,
            TX1p: landpattern.A2,
            TX1n: landpattern.A3,
            VBUS[0]: landpattern.A4,
            CC1: landpattern.A5,
            DA: landpattern.A6,
            D_A: landpattern.A7,
            SBU1: landpattern.A8,
            VBUS[1]: landpattern.A9,
            RX2n: landpattern.A10,
            RX2p: landpattern.A11,
            GND[1]: landpattern.A12,
            GND[2]: landpattern.B1,
            TX2p: landpattern.B2,
            TX2n: landpattern.B3,
            VBUS[2]: landpattern.B4,
            CC2: landpattern.B5,
            DB: landpattern.B6,
            D_B: landpattern.B7,
            SBU2: landpattern.B8,
            VBUS[3]: landpattern.B9,
            RX1n: landpattern.B10,
            RX1p: landpattern.B11,
            GND[3]: landpattern.B12,
            SHIELDA: [
                landpattern.S4,
                landpattern.S3,
                landpattern.S2,
                landpattern.S1,
            ],
            SHIELDB: [
                landpattern.S14,
                landpattern.S13,
                landpattern.S12,
                landpattern.S11,
            ],
        }),
    ]

Device: type[Comp_10132328_10011LF] = Comp_10132328_10011LF

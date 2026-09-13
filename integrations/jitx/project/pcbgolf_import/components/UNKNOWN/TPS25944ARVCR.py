# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/components/UNKNOWN/TPS25944ARVCR.py 
# To import this component:
#     from .components.UNKNOWN import TPS25944ARVCR
#     u1 = TPS25944ARVCR.TPS25944ARVCR()
from jitx.landpattern import Landpattern, Pad
from jitx.model3d import Model3D
from jitx.symbol import Symbol, Pin, Direction
from jitx.component import Component
from jitx.net import Port
from jitx.landpattern import PadMapping
from jitx.symbol import SymbolMapping
from jitx.feature import Silkscreen, Paste, Soldermask
from jitx.shapes.primitive import Polyline, Arc, ArcPolyline
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


class RectSmdPad_1(Pad):
    shape = rectangle(0.2, 0.6)
    paste = [
        Paste(rectangle(0.2, 0.6)),
    ]
    soldermask = [
        Soldermask(rectangle(0.2, 0.6)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class RectSmdPad_2(Pad):
    shape = rectangle(1.6, 2.6)
    paste = [
        Paste(rectangle(1.6, 2.6)),
    ]
    soldermask = [
        Soldermask(rectangle(1.6, 2.6)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class LandpatternWQFN20(Landpattern):
    p = {
        1: RectSmdPad_1().at(Transform((-1.4, 1.25), 90)),
        2: RectSmdPad_1().at(Transform((-1.4, 0.75), 90)),
        3: RectSmdPad_1().at(Transform((-1.4, 0.25), 90)),
        4: RectSmdPad_1().at(Transform((-1.4, -0.25), 90)),
        5: RectSmdPad_1().at(Transform((-1.4, -0.75), 90)),
        6: RectSmdPad_1().at(Transform((-1.4, -1.25), 90)),
        7: RectSmdPad_1().at(Transform((-0.75, -1.9), 180)),
        8: RectSmdPad_1().at(Transform((-0.25, -1.9), 180)),
        9: RectSmdPad_1().at(Transform((0.25, -1.9), 180)),
        10: RectSmdPad_1().at(Transform((0.75, -1.9), 180)),
        11: RectSmdPad_1().at(Transform((1.4, -1.25), 270)),
        12: RectSmdPad_1().at(Transform((1.4, -0.75), 270)),
        13: RectSmdPad_1().at(Transform((1.4, -0.25), 270)),
        14: RectSmdPad_1().at(Transform((1.4, 0.25), 270)),
        15: RectSmdPad_1().at(Transform((1.4, 0.75), 270)),
        16: RectSmdPad_1().at(Transform((1.4, 1.25), 270)),
        17: RectSmdPad_1().at((0.75, 1.9)),
        18: RectSmdPad_1().at((0.25, 1.9)),
        19: RectSmdPad_1().at((-0.25, 1.9)),
        20: RectSmdPad_1().at((-0.75, 1.9)),
    }
    PAD = RectSmdPad_2().at((0, 0))

    silkscreen = [
        Silkscreen(Polyline(0.127, [(1.5, 2), (1.5, 1.655)])),
        Silkscreen(Polyline(0.127, [(1.155, 2), (1.5, 2)])),
        Silkscreen(Polyline(0.127, [(-1.155, 2), (-1.5, 2)])),
        Silkscreen(Polyline(0.127, [(-1.5, 2), (-1.5, 1.655)])),
        Silkscreen(Polyline(0.127, [(1.5, -1.655), (1.5, -2)])),
        Silkscreen(Polyline(0.127, [(-1.5, -1.655), (-1.5, -2)])),
        Silkscreen(Polyline(0.127, [(1.5, -2), (1.155, -2)])),
        Silkscreen(Polyline(0.127, [(-1.5, -2), (-1.155, -2)])),
        Silkscreen(ArcPolyline(0.3048, [
            Arc((-2.227, 1.4), 0.14142, 0, 360)])),
    ]

    models = [
        Model3D("QFN-20-1EP_3x4mm_P0.5mm_EP1.65x2.65mm.step",
            position=(0, 0, 0),
            scale=(1, 1, 1),
            rotation=(0, 0, 0),
        ),
    ]

class Symbolcomma_ai_11112255_TPS25942(Symbol):
    pin_name_size = 1.2
    DMODE = Pin((0, 6), 4, Direction.Left, pin_name_size=1.2)
    PG = Pin((20, 6), 4, Direction.Right, pin_name_size=1.2)
    PGTH = Pin((20, 4), 4, Direction.Right, pin_name_size=1.2)
    VOUT = Pin((20, 16), 4, Direction.Right, pin_name_size=0)
    VIN = Pin((0, 16), 4, Direction.Left, pin_name_size=0)
    EN = Pin((0, 12), 4, Direction.Left, pin_name_size=1.2)
    OVP = Pin((0, 10), 4, Direction.Left, pin_name_size=1.2)
    ILIM = Pin((0, 4), 4, Direction.Left, pin_name_size=1.2)
    DVDT = Pin((0, 2), 4, Direction.Left, pin_name_size=1.2)
    IMON = Pin((20, 10), 4, Direction.Right, pin_name_size=1.2)
    FLT_N = Pin((20, 8), 4, Direction.Right, pin_name_size=1.2)
    GND = Pin((20, 2), 4, Direction.Right, pin_name_size=0)
    draws = [
        Polyline(0.254, [(0, 0), (20, 0)]),
        Polyline(0.254, [(20, 18), (0, 18)]),
        Polyline(0.254, [(0, 18), (0, 0)]),
        Polyline(0.254, [(20, 0), (20, 18)]),
    ]

class TPS25944ARVCR(Component):
    description = ""
    mpn = "TPS25944ARVCR"
    datasheet = ""
    reference_designator_prefix = "U"
    landpattern = LandpatternWQFN20()
    DMODE = Port()
    PG = Port()
    PGTH = Port()
    VOUT = Port()
    VIN = Port()
    EN = Port()
    OVP = Port()
    ILIM = Port()
    DVDT = Port()
    IMON = Port()
    FLT_N = Port()
    GND = Port()
    symbol = Symbolcomma_ai_11112255_TPS25942()
    mappings = [
        SymbolMapping({
            DMODE: symbol.DMODE, 
            PG: symbol.PG, 
            PGTH: symbol.PGTH, 
            VOUT: symbol.VOUT, 
            VIN: symbol.VIN, 
            EN: symbol.EN, 
            OVP: symbol.OVP, 
            ILIM: symbol.ILIM, 
            DVDT: symbol.DVDT, 
            IMON: symbol.IMON, 
            FLT_N: symbol.FLT_N, 
            GND: symbol.GND
        }),
        PadMapping({
            DMODE: landpattern.p[1],
            PG: landpattern.p[2],
            PGTH: landpattern.p[3],
            VOUT: [
                landpattern.p[8],
                landpattern.p[7],
                landpattern.p[6],
                landpattern.p[5],
                landpattern.p[4],
            ],
            VIN: [
                landpattern.p[13],
                landpattern.p[12],
                landpattern.p[11],
                landpattern.p[10],
                landpattern.p[9],
            ],
            EN: landpattern.p[14],
            OVP: landpattern.p[15],
            ILIM: landpattern.p[17],
            DVDT: landpattern.p[18],
            IMON: landpattern.p[19],
            FLT_N: landpattern.p[20],
            GND: [
                landpattern.PAD,
                landpattern.p[16],
            ],
        }),
    ]

Device: type[TPS25944ARVCR] = TPS25944ARVCR

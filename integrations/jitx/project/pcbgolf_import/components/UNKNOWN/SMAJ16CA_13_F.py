# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/components/UNKNOWN/SMAJ16CA_13_F.py 
# To import this component:
#     from .components.UNKNOWN import SMAJ16CA_13_F
#     u1 = SMAJ16CA_13_F.SMAJ16CA_13_F()
from jitx.landpattern import Landpattern, Pad
from jitx.model3d import Model3D
from jitx.symbol import Symbol, Pin, Direction
from jitx.component import Component
from jitx.net import Port
from jitx.landpattern import PadMapping
from jitx.symbol import SymbolMapping
from jitx.feature import Silkscreen, Paste, Soldermask
from jitx.anchor import Anchor
from jitx.shapes.primitive import Polyline, Arc, ArcPolyline, Text
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


class RectSmdPad(Pad):
    shape = rectangle(2.159, 2.743)
    paste = [
        Paste(rectangle(2.159, 2.743)),
    ]
    soldermask = [
        Soldermask(rectangle(2.159, 2.743)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class LandpatternDO_214AA_SMB_(Landpattern):
    p = {
        1: RectSmdPad().at((-2.21, 0)),
        2: RectSmdPad().at((2.21, 0)),
    }

    silkscreen = [
        Silkscreen(Polyline(0.1524, [(-2.16, -1.78), (2.16, -1.78)])),
        Silkscreen(Polyline(0.1524, [(-2.16, 1.78), (2.16, 1.78)])),
        Silkscreen(ArcPolyline(0.3048, [
            Arc((-3.04, -2.07), 0.1, 0, 360)])),
    ]

    models = [
        Model3D("D_SMB.step",
            position=(0, 0, 0),
            scale=(1, 1, 1),
            rotation=(0, 0, 0),
        ),
    ]

class Symbolcomma_ai_11112255_TVS_BI_DO214AA(Symbol):
    pin_name_size = 0
    pad_name_size = 0
    p = {
        1: Pin((-2, 0), 0, Direction.Left),
        2: Pin((4, 0), 0, Direction.Right),
    }
    draws = [
        Text(">REF", 1.19, Anchor.W).at(Transform((-2, 2.38), 270)),
        Text(">VALUE", 1.19, Anchor.W).at(Transform((-2, -3.62), 270)),
        Text("pcbgolf:DO-214AA(SMB)", 1, Anchor.C).at(Transform((0, 0), 270)),
        Text("", 1, Anchor.C).at(Transform((0, 0), 270)),
        Polyline(0.254, [(3, 0), (3, 1)]),
        Polyline(0.1524, [(-2, 0), (-1, 0)]),
        Polyline(0.254, [(3, 1), (1, 0)]),
        Polyline(0.254, [(-1, 0), (-1, -1)]),
        Polyline(0.254, [(1, 0), (3, -1)]),
        Polyline(0.254, [(1, 0), (1, -1)]),
        Polyline(0.254, [(1, 0), (-1, 1)]),
        Polyline(0.254, [(1, 1), (1.4, 1.2)]),
        Polyline(0.254, [(-1, 1), (-1, 0)]),
        Polyline(0.254, [(-1, -1), (1, 0)]),
        Polyline(0.254, [(1, -1), (0.6, -1.2)]),
        Polyline(0.1524, [(4, 0), (3, 0)]),
        Polyline(0.254, [(3, -1), (3, 0)]),
        Polyline(0.254, [(1, 1), (1, 0)]),
    ]
    if False : # hidden objects
        draw_hidden = Text("ki_locked: ", 1, Anchor.C)

class SMAJ16CA_13_F(Component):
    description = ""
    mpn = "SMAJ16CA-13-F"
    datasheet = ""
    reference_designator_prefix = "D1"
    landpattern = LandpatternDO_214AA_SMB_()
    p = {
        1: Port(),
        2: Port(),
    }
    symbol = Symbolcomma_ai_11112255_TVS_BI_DO214AA()
    mappings = [
        SymbolMapping({
            p[1]: symbol.p[1], 
            p[2]: symbol.p[2]
        }),
        PadMapping({
            p[1]: landpattern.p[1],
            p[2]: landpattern.p[2],
        }),
    ]

Device: type[SMAJ16CA_13_F] = SMAJ16CA_13_F

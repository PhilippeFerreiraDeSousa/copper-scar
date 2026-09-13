# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/components/UNKNOWN/CLMVC_FKA_CL1D1L71BB7C3C3.py 
# To import this component:
#     from .components.UNKNOWN import CLMVC_FKA_CL1D1L71BB7C3C3
#     u1 = CLMVC_FKA_CL1D1L71BB7C3C3.CLMVC_FKA_CL1D1L71BB7C3C3()
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
    shape = rectangle(1, 0.8)
    paste = [
        Paste(rectangle(1, 0.8)),
    ]
    soldermask = [
        Soldermask(rectangle(1, 0.8)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class LandpatternCREE_RGB_CLMVC(Landpattern):
    U1 = RectSmdPad().at((-0.75, 0.55))
    U2 = RectSmdPad().at((-0.75, -0.55))
    U3 = RectSmdPad().at((0.75, -0.55))
    U4 = RectSmdPad().at((0.75, 0.55))

    silkscreen = [
        Silkscreen(Polyline(0.127, [(-1.25, 1.1), (1.25, 1.1)])),
        Silkscreen(Polyline(0.127, [(1.25, -1.1), (-1.25, -1.1)])),
        Silkscreen(ArcPolyline(0.127, [
            Arc((-1.27, 1.12), 0.1, 0, 360)])),
    ]

    models = [
        Model3D("CLMVC-FKA-CL1D1L71BB7C3C3.step",
            position=(0, 0, 0),
            scale=(1, 1, 1),
            rotation=(-90, 0, 0),
        ),
    ]

class Symbolcomma_ai_11112255_CREE_RGB_CLMVC(Symbol):
    pin_name_size = 1.2
    pad_name_size = 1.2
    COMp = Pin((-8, -4), 4, Direction.Left)
    Rn = Pin((-8, 4), 4, Direction.Left)
    Gn = Pin((6, 4), 4, Direction.Right)
    Bn = Pin((6, -4), 4, Direction.Right)
    draws = [
        Text(">REF", 1.19, Anchor.W).at((-5, 8.8)),
        Text(">VALUE", 1, Anchor.C),
        Text("pcbgolf:CREE-RGB-CLMVC", 1, Anchor.C),
        Text("", 1, Anchor.C),
        Polyline(0.254, [(-8, -8), (6, -8)]),
        Polyline(0.254, [(6, 8), (-8, 8)]),
        Polyline(0.254, [(-8, 8), (-8, -8)]),
        Polyline(0.254, [(6, -8), (6, 8)]),
    ]
    if False : # hidden objects
        draw_hidden = Text("ki_locked: ", 1, Anchor.C)

class CLMVC_FKA_CL1D1L71BB7C3C3(Component):
    description = ""
    mpn = "CLMVC-FKA-CL1D1L71BB7C3C3"
    datasheet = ""
    reference_designator_prefix = "LED1"
    landpattern = LandpatternCREE_RGB_CLMVC()
    COMp = Port()
    Rn = Port()
    Gn = Port()
    Bn = Port()
    symbol = Symbolcomma_ai_11112255_CREE_RGB_CLMVC()
    mappings = [
        SymbolMapping({
            COMp: symbol.COMp, 
            Rn: symbol.Rn, 
            Gn: symbol.Gn, 
            Bn: symbol.Bn
        }),
        PadMapping({
            COMp: landpattern.U1,
            Rn: landpattern.U2,
            Gn: landpattern.U3,
            Bn: landpattern.U4,
        }),
    ]

Device: type[CLMVC_FKA_CL1D1L71BB7C3C3] = CLMVC_FKA_CL1D1L71BB7C3C3

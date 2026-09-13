# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/components/UNKNOWN/PMEG10020ELRX.py 
# To import this component:
#     from .components.UNKNOWN import PMEG10020ELRX
#     u1 = PMEG10020ELRX.PMEG10020ELRX()
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
    shape = rectangle(1.2, 0.85)
    paste = [
        Paste(rectangle(1.2, 0.85)),
    ]
    soldermask = [
        Soldermask(rectangle(1.2, 0.85)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class LandpatternSOD_123F(Landpattern):
    p = {
        1: RectSmdPad().at((0, -1.5)),
        2: RectSmdPad().at((0, 1.5)),
    }

    silkscreen = [
        Silkscreen(Polyline(0.127, [(-0.8, -1.3), (-0.8, 1.3)])),
        Silkscreen(Polyline(0.127, [(0.8, 1.3), (0.8, -1.3)])),
        Silkscreen(ArcPolyline(0.127, [
            Arc((-0.946, -1.6), 0.1, 0, 360)])),
    ]

    models = [
        Model3D("D_SOD-123F.step",
            position=(0, 0, 0),
            scale=(1, 1, 1),
            rotation=(0, 0, -90),
        ),
    ]

class Symbolcomma_ai_11112255_DIODEDB2W40100L(Symbol):
    pin_name_size = 0
    pad_name_size = 0
    C = Pin((2, 0), 0, Direction.Right)
    A = Pin((-2, 0), 0, Direction.Left)
    draws = [
        Text(">REF", 1.19, Anchor.W).at((2, 0.38)),
        Text(">VALUE", 1, Anchor.C),
        Text("pcbgolf:SOD-123F", 1, Anchor.C),
        Text("", 1, Anchor.C),
        Polyline(0.254, [(1, 0), (-1, 1)]),
        Polyline(0.254, [(1, 0), (1, -1)]),
        Polyline(0.254, [(1, 1), (1, 0)]),
        Polyline(0.254, [(-1, -1), (1, 0)]),
        Polyline(0.254, [(-1, 0), (-1, -1)]),
        Polyline(0.254, [(-1, 1), (-1, 0)]),
        Polyline(0.1524, [(-2, 0), (-1, 0)]),
        Polyline(0.1524, [(2, 0), (1, 0)]),
    ]
    if False : # hidden objects
        draw_hidden = Text("ki_locked: ", 1, Anchor.C)

class PMEG10020ELRX(Component):
    description = ""
    mpn = "PMEG10020ELRX"
    datasheet = ""
    reference_designator_prefix = "D2"
    landpattern = LandpatternSOD_123F()
    C = Port()
    A = Port()
    symbol = Symbolcomma_ai_11112255_DIODEDB2W40100L()
    mappings = [
        SymbolMapping({
            C: symbol.C, 
            A: symbol.A
        }),
        PadMapping({
            C: landpattern.p[1],
            A: landpattern.p[2],
        }),
    ]

Device: type[PMEG10020ELRX] = PMEG10020ELRX

# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/components/UNKNOWN/comma_ai_11112255_M2_BOLT.py 
# To import this component:
#     from .components.UNKNOWN import comma_ai_11112255_M2_BOLT
#     u1 = comma_ai_11112255_M2_BOLT.comma_ai_11112255_M2_BOLT()
from jitx.landpattern import Landpattern, Pad
from jitx.symbol import Symbol, Pin, Direction
from jitx.component import Component
from jitx.net import Port
from jitx.landpattern import PadMapping
from jitx.symbol import SymbolMapping
from jitx.feature import Cutout, Soldermask
from jitx.layerindex import Side
from jitx.shapes.primitive import Circle

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


class CircleThPad(Pad):
    shape = Circle(radius=2.1)
    cutout = [
        Cutout(Circle(radius=1)),
    ]
    soldermask = [
        Soldermask(Circle(radius=2.1)),
        Soldermask(Circle(radius=2.1), side=Side.Bottom),
    ]
    def __init__(self):
        self.solder = make_soldermask(self.shape, amount=0.0508, thruhole=True)

class LandpatternM2_BOLT(Landpattern):
    p = {
        0: CircleThPad().at((0, 0)),
    }

class Symbolcomma_ai_11112255_M2_BOLT(Symbol):
    pin_name_size = 0
    pad_name_size = 0
    p = {
        1: Pin((-2, 0), 2, Direction.Left),
    }
    draw = Circle(radius=2)

class comma_ai_11112255_M2_BOLT(Component):
    description = ""
    mpn = "comma.ai_11112255_M2_BOLT"
    datasheet = ""
    reference_designator_prefix = "BH"
    landpattern = LandpatternM2_BOLT()
    p = {
        1: Port(),
    }
    symbol = Symbolcomma_ai_11112255_M2_BOLT()
    mappings = [
        SymbolMapping({
            p[1]: symbol.p[1]
        }),
        PadMapping({
            p[1]: landpattern.p[0],
        }),
    ]

Device: type[comma_ai_11112255_M2_BOLT] = comma_ai_11112255_M2_BOLT

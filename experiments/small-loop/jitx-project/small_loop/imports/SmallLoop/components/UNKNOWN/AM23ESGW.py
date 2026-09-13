# File Location: .local/small-loop/jitx/small_loop/imports/SmallLoop/components/UNKNOWN/AM23ESGW.py 
# To import this component:
#     from .components.UNKNOWN import AM23ESGW
#     u1 = AM23ESGW.AM23ESGW()
from jitx.landpattern import Landpattern, Pad
from jitx.model3d import Model3D
from jitx.symbol import Symbol, Pin, Direction
from jitx.component import Component
from jitx.net import Port
from jitx.landpattern import PadMapping
from jitx.symbol import SymbolMapping
from jitx.feature import Silkscreen, Paste, Soldermask
from jitx.anchor import Anchor
from jitx.shapes.primitive import Polyline, Polygon, Text
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
    shape = rectangle(0.8, 0.9)
    paste = [
        Paste(rectangle(0.8, 0.9)),
    ]
    soldermask = [
        Soldermask(rectangle(0.8, 0.9)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class LandpatternSOT23_3(Landpattern):
    p = {
        1: RectSmdPad().at((-0.95, -1)),
        2: RectSmdPad().at((0.95, -1)),
        3: RectSmdPad().at((0, 1.1)),
    }

    silkscreen = [
        Silkscreen(Polyline(0.127, [(-1.7, 0.7), (-1.7, -0.5)])),
        Silkscreen(Polyline(0.127, [(-1.7, 0.7), (-0.6, 0.7)])),
        Silkscreen(Polyline(0.127, [(-1.7, -0.5), (-1.6, -0.5)])),
        Silkscreen(Polyline(0.127, [(0.6, 0.7), (1.7, 0.7)])),
        Silkscreen(Polyline(0.127, [(1.7, 0.7), (1.7, -0.5)])),
        Silkscreen(Polyline(0.127, [(1.7, -0.5), (1.6, -0.5)])),
    ]

    # Model3D file not found: "${KIPRJMOD}/pcbgolf.3dshapes/Package_TO_SOT_SMD.3dshapes/SOT-23-3.step"

class Symbolcomma_ai_11112255_LED_CC_GREEN_RED_AM23ESG(Symbol):
    pin_name_size = 0
    pad_name_size = 0
    AR = Pin((2, 4), 2, Direction.Up)
    AG = Pin((-2, 4), 2, Direction.Up)
    C = Pin((0, 0), 2, Direction.Down)
    draws = [
        Text(">REF", 1.19, Anchor.E).at((0, 6.29921)),
        Text(">VALUE", 1, Anchor.C).at((0, 4.72441)),
        Text("pcbgolf:SOT23-3", 1, Anchor.C).at((0, 3.14961)),
        Text("", 1, Anchor.C).at((0, 1.5748)),
        Polyline(0.254, [(3, 2), (2, 2)]),
        Polyline(0.254, [(-1, 2), (-2, 2)]),
        Polyline(0.254, [(-2, 0), (2, 0)]),
        Polyline(0.1524, [(-3.6, 3.4), (-4.7, 2.3)]),
        Polyline(0.254, [(2, 0), (2, 2)]),
        Polyline(0.254, [(2, 2), (1, 2)]),
        Polyline(0.254, [(-2, 2), (-3, 4)]),
        Polyline(0.1524, [(0.5, 2.5), (-0.6, 1.4)]),
        Polygon([
            (-4.7, 2.3),
            (-4.4, 3),
            (-4, 2.6),
            (-4.7, 2.3)]),
        Polyline(0.254, [(-2, 2), (-2, 0)]),
        Polygon([
            (-0.6, 1.4),
            (-0.3, 2.1),
            (0.1, 1.7),
            (-0.6, 1.4)]),
        Polyline(0.254, [(-1, 4), (-2, 2)]),
        Polygon([
            (-0.7, 2.3),
            (-0.4, 3),
            (0, 2.6),
            (-0.7, 2.3)]),
        Polygon([
            (-4.6, 1.4),
            (-4.3, 2.1),
            (-3.9, 1.7),
            (-4.6, 1.4)]),
        Polyline(0.254, [(3, 4), (2, 2)]),
        Polyline(0.254, [(-1, 4), (-3, 4)]),
        Polyline(0.1524, [(0.4, 3.4), (-0.7, 2.3)]),
        Polyline(0.254, [(2, 2), (1, 4)]),
        Polyline(0.254, [(-2, 2), (-3, 2)]),
        Polyline(0.254, [(3, 4), (1, 4)]),
        Polyline(0.1524, [(-3.5, 2.5), (-4.6, 1.4)]),
        Text("G", 1.19, Anchor.W).at((-3.6, 0)),
        Text("R", 1.19, Anchor.W).at((2.6, 0)),
    ]
    if False : # hidden objects
        draw_hidden = Text("ki_locked: ", 1, Anchor.C)

class AM23ESGW(Component):
    description = ""
    mpn = "AM23ESGW"
    datasheet = ""
    reference_designator_prefix = "LED10"
    landpattern = LandpatternSOT23_3()
    AR = Port()
    AG = Port()
    C = Port()
    symbol = Symbolcomma_ai_11112255_LED_CC_GREEN_RED_AM23ESG()
    mappings = [
        SymbolMapping({
            AR: symbol.AR, 
            AG: symbol.AG, 
            C: symbol.C
        }),
        PadMapping({
            AR: landpattern.p[1],
            AG: landpattern.p[2],
            C: landpattern.p[3],
        }),
    ]

Device: type[AM23ESGW] = AM23ESGW

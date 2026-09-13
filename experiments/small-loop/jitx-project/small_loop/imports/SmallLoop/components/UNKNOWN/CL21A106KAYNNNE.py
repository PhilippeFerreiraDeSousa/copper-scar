# File Location: .local/small-loop/jitx/small_loop/imports/SmallLoop/components/UNKNOWN/CL21A106KAYNNNE.py 
# To import this component:
#     from .components.UNKNOWN import CL21A106KAYNNNE
#     u1 = CL21A106KAYNNNE.CL21A106KAYNNNE()
from jitx.landpattern import Landpattern, Pad
from jitx.model3d import Model3D
from jitx.symbol import Symbol, Pin, Direction
from jitx.component import Component
from jitx.net import Port
from jitx.landpattern import PadMapping
from jitx.symbol import SymbolMapping
from jitx.feature import Silkscreen, Custom, Paste, Soldermask
from jitx.anchor import Anchor
from jitx.shapes.primitive import Polyline, Polygon, Text
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
    shape = rectangle(0.8, 1.2)
    paste = [
        Paste(rectangle(0.8, 1.2)),
    ]
    soldermask = [
        Soldermask(rectangle(0.8, 1.2)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class LandpatternU0805_C(Landpattern):
    p = {
        1: RectSmdPad().at((-0.9, 0)),
        2: RectSmdPad().at((0.9, 0)),
    }

    customlayer = [
        Custom(Polygon([
            (0.508, -0.635),
            (1.016, -0.635),
            (1.016, 0.635),
            (0.508, 0.635)]), name="Fab"),
        Custom(Polygon([
            (-0.508, 0.635),
            (-1.016, 0.635),
            (-1.016, -0.635),
            (-0.508, -0.635)]), name="Fab"),
    ]
    silkscreen = [
        Silkscreen(Polyline(0.127, [(1.5, -0.8), (1.5, 0.8)])),
        Silkscreen(Polyline(0.127, [(1.5, 0.8), (-1.5, 0.8)])),
        Silkscreen(Polyline(0.127, [(-1.5, -0.8), (1.5, -0.8)])),
        Silkscreen(Polyline(0.127, [(-1.5, 0.8), (-1.5, -0.8)])),
    ]

    # Model3D file not found: "${KIPRJMOD}/pcbgolf.3dshapes/Capacitor_SMD.3dshapes/C_0805_2012Metric.step"

class Symbolcomma_ai_11112255_C0805(Symbol):
    pin_name_size = 0
    pad_name_size = 0
    p = {
        1: Pin((0, 2), 2, Direction.Up),
        2: Pin((0, 0), 2, Direction.Down),
    }
    draws = [
        Text(">REF", 1.19, Anchor.W).at((0, 6.29921)),
        Text(">VALUE", 1.19, Anchor.W).at((0, 4.72441)),
        Text("pcbgolf:0805-C", 1, Anchor.C).at((0, 3.14961)),
        Text("", 1, Anchor.C).at((0, 1.5748)),
        Transform((0, 0.6)) * rectangle(3.2, 0.4),
        Polyline(0.1524, [(0, 2), (0, 1.6)]),
        Transform((0, 1.4)) * rectangle(3.2, 0.4),
        Polyline(0.1524, [(0, 0), (0, 0.4)]),
    ]
    if False : # hidden objects
        draw_hidden = Text("ki_locked: ", 1, Anchor.C)

class CL21A106KAYNNNE(Component):
    description = ""
    mpn = "CL21A106KAYNNNE"
    datasheet = ""
    reference_designator_prefix = "C50"
    landpattern = LandpatternU0805_C()
    p = {
        1: Port(),
        2: Port(),
    }
    symbol = Symbolcomma_ai_11112255_C0805()
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

Device: type[CL21A106KAYNNNE] = CL21A106KAYNNNE

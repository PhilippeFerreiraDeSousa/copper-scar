# File Location: .local/small-loop/jitx/small_loop/imports/SmallLoop/components/UNKNOWN/CL05F104ZO5NNNC.py 
# To import this component:
#     from .components.UNKNOWN import CL05F104ZO5NNNC
#     u1 = CL05F104ZO5NNNC.CL05F104ZO5NNNC()
from jitx.landpattern import Landpattern, Pad
from jitx.model3d import Model3D
from jitx.symbol import Symbol, Pin, Direction
from jitx.component import Component
from jitx.net import Port
from jitx.landpattern import PadMapping
from jitx.symbol import SymbolMapping
from jitx.feature import Silkscreen, Custom, Paste, Courtyard, Glue, Soldermask
from jitx.shapes.primitive import Polyline, Polygon
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
    shape = rectangle(0.6, 0.6)
    paste = [
        Paste(rectangle(0.6, 0.6)),
    ]
    soldermask = [
        Soldermask(rectangle(0.6, 0.6)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class LandpatternU0402_C(Landpattern):
    p = {
        1: RectSmdPad().at((-0.45, 0)),
        2: RectSmdPad().at((0.45, 0)),
    }

    customlayer = [
        Custom(Polyline(0.1524, [(-0.245, 0.224), (0.245, 0.224)]), name="Fab"),
        Custom(Polyline(0.1524, [(0.245, -0.224), (-0.245, -0.224)]), name="Fab"),
        Custom(Polygon([
            (-0.554, -0.3048),
            (-0.254, -0.3048),
            (-0.254, 0.2951),
            (-0.554, 0.2951)]), name="Fab"),
        Custom(Polygon([
            (0.2588, -0.3048),
            (0.5588, -0.3048),
            (0.5588, 0.2951),
            (0.2588, 0.2951)]), name="Fab"),
    ]
    silkscreen = [
        Silkscreen(Polyline(0.127, [(-0.9, 0.45), (-0.9, -0.45)])),
        Silkscreen(Polyline(0.127, [(-0.9, -0.45), (0.9, -0.45)])),
        Silkscreen(Polyline(0.127, [(0.9, 0.45), (-0.9, 0.45)])),
        Silkscreen(Polyline(0.127, [(0.9, -0.45), (0.9, 0.45)])),
    ]
    courtyard = [
        Courtyard(Polygon([
            (-0.973, 0.483),
            (0.973, 0.483),
            (0.973, -0.483),
            (-0.973, -0.483)])),
    ]
    glue = [
        Glue(Polygon([
            (-0.1999, -0.4001),
            (0.1999, -0.4001),
            (0.1999, 0.4001),
            (-0.1999, 0.4001)])),
    ]

    # Model3D file not found: "${KIPRJMOD}/pcbgolf.3dshapes/Capacitor_SMD.3dshapes/C_0402_1005Metric.step"

class Symbolcomma_ai_11112255_C0402(Symbol):
    pin_name_size = 0
    pad_name_size = 0
    p = {
        1: Pin((0, 2), 2, Direction.Up),
        2: Pin((0, 0), 2, Direction.Down),
    }
    draws = [
        Transform((0, 0.6)) * rectangle(3.2, 0.4),
        Polyline(0.1524, [(0, 2), (0, 1.6)]),
        Transform((0, 1.4)) * rectangle(3.2, 0.4),
        Polyline(0.1524, [(0, 0), (0, 0.4)]),
    ]

class CL05F104ZO5NNNC(Component):
    description = ""
    mpn = "CL05F104ZO5NNNC"
    datasheet = ""
    reference_designator_prefix = "C"
    landpattern = LandpatternU0402_C()
    p = {
        1: Port(),
        2: Port(),
    }
    symbol = Symbolcomma_ai_11112255_C0402()
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

Device: type[CL05F104ZO5NNNC] = CL05F104ZO5NNNC

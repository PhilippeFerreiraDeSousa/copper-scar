# File Location: .local/small-loop/jitx/small_loop/imports/SmallLoop/landpatterns/LandpatternTDFN8_2X3MC_MCH.py 
from jitx.landpattern import Landpattern, Pad
from jitx.model3d import Model3D
from jitx.feature import Silkscreen, Paste, Soldermask
from jitx.shapes.primitive import Polyline, Arc, ArcPolyline
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


class RectSmdPad_1(Pad):
    shape = rectangle(0.7572, 0.2548)
    paste = [
        Paste(rectangle(0.7572, 0.2548)),
    ]
    soldermask = [
        Soldermask(rectangle(0.7572, 0.2548)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class RectSmdPad_2(Pad):
    shape = rectangle(1.6002, 1.6002)
    paste = [
        Paste(rectangle(1.6002, 1.6002)),
    ]
    soldermask = [
        Soldermask(rectangle(1.6002, 1.6002)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class LandpatternTDFN8_2X3MC_MCH(Landpattern):
    p = {
        1: RectSmdPad_1().at((-1.42, 0.75)),
        2: RectSmdPad_1().at((-1.42, 0.25)),
        3: RectSmdPad_1().at((-1.42, -0.25)),
        4: RectSmdPad_1().at((-1.42, -0.75)),
        5: RectSmdPad_1().at((1.42, -0.75)),
        6: RectSmdPad_1().at((1.42, -0.25)),
        7: RectSmdPad_1().at((1.42, 0.25)),
        8: RectSmdPad_1().at((1.42, 0.75)),
    }
    PAD = RectSmdPad_2().at((0, 0))

    silkscreen = [
        Silkscreen(Polyline(0.1524, [(1.4986, 1.016), (0.3048, 1.016)])),
        Silkscreen(Polyline(0.1524, [(0.3048, 1.016), (-1.4986, 1.016)])),
        Silkscreen(Polyline(0.1524, [(-1.4986, 1.016), (-1.4986, -1.016)])),
        Silkscreen(Polyline(0.1524, [(1.4986, -1.016), (1.4986, 1.016)])),
        Silkscreen(Polyline(0.1524, [(-1.4986, -1.016), (1.4986, -1.016)])),
        Silkscreen(ArcPolyline(0.1524, [
            Arc((-0, 1.0033), 0.30506, 2.38594, -180)])),
    ]

    # Model3D file not found: "${KIPRJMOD}/pcbgolf.3dshapes/Package_DFN_QFN.3dshapes/DFN-8-1EP_3x2mm_P0.5mm_EP1.7x1.6mm.step"


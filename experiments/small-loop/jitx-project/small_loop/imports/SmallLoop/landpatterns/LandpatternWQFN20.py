# File Location: .local/small-loop/jitx/small_loop/imports/SmallLoop/landpatterns/LandpatternWQFN20.py 
from jitx.landpattern import Landpattern, Pad
from jitx.model3d import Model3D
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

    # Model3D file not found: "${KIPRJMOD}/pcbgolf.3dshapes/Package_DFN_QFN.3dshapes/QFN-20-1EP_3x4mm_P0.5mm_EP1.65x2.65mm.step"


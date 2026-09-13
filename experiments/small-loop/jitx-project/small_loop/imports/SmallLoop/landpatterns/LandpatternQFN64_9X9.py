# File Location: .local/small-loop/jitx/small_loop/imports/SmallLoop/landpatterns/LandpatternQFN64_9X9.py 
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
    shape = rectangle(0.28, 0.69)
    paste = [
        Paste(rectangle(0.28, 0.69)),
    ]
    soldermask = [
        Soldermask(rectangle(0.28, 0.69)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class RectSmdPad_2(Pad):
    shape = rectangle(4.7, 4.7)
    paste = [
        Paste(rectangle(4.7, 4.7)),
    ]
    soldermask = [
        Soldermask(rectangle(4.7, 4.7)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class LandpatternQFN64_9X9(Landpattern):
    p = {
        1: RectSmdPad_1().at(Transform((-4.35, 3.75), 90)),
        2: RectSmdPad_1().at(Transform((-4.35, 3.25), 90)),
        3: RectSmdPad_1().at(Transform((-4.35, 2.75), 90)),
        4: RectSmdPad_1().at(Transform((-4.35, 2.25), 90)),
        5: RectSmdPad_1().at(Transform((-4.35, 1.75), 90)),
        6: RectSmdPad_1().at(Transform((-4.35, 1.25), 90)),
        7: RectSmdPad_1().at(Transform((-4.35, 0.75), 90)),
        8: RectSmdPad_1().at(Transform((-4.35, 0.25), 90)),
        9: RectSmdPad_1().at(Transform((-4.35, -0.25), 90)),
        10: RectSmdPad_1().at(Transform((-4.35, -0.75), 90)),
        11: RectSmdPad_1().at(Transform((-4.35, -1.25), 90)),
        12: RectSmdPad_1().at(Transform((-4.35, -1.75), 90)),
        13: RectSmdPad_1().at(Transform((-4.35, -2.25), 90)),
        14: RectSmdPad_1().at(Transform((-4.35, -2.75), 90)),
        15: RectSmdPad_1().at(Transform((-4.35, -3.25), 90)),
        16: RectSmdPad_1().at(Transform((-4.35, -3.75), 90)),
        17: RectSmdPad_1().at(Transform((-3.75, -4.35), 180)),
        18: RectSmdPad_1().at(Transform((-3.25, -4.35), 180)),
        19: RectSmdPad_1().at(Transform((-2.75, -4.35), 180)),
        20: RectSmdPad_1().at(Transform((-2.25, -4.35), 180)),
        21: RectSmdPad_1().at(Transform((-1.75, -4.35), 180)),
        22: RectSmdPad_1().at(Transform((-1.25, -4.35), 180)),
        23: RectSmdPad_1().at(Transform((-0.75, -4.35), 180)),
        24: RectSmdPad_1().at(Transform((-0.25, -4.35), 180)),
        25: RectSmdPad_1().at(Transform((0.25, -4.35), 180)),
        26: RectSmdPad_1().at(Transform((0.75, -4.35), 180)),
        27: RectSmdPad_1().at(Transform((1.25, -4.35), 180)),
        28: RectSmdPad_1().at(Transform((1.75, -4.35), 180)),
        29: RectSmdPad_1().at(Transform((2.25, -4.35), 180)),
        30: RectSmdPad_1().at(Transform((2.75, -4.35), 180)),
        31: RectSmdPad_1().at(Transform((3.25, -4.35), 180)),
        32: RectSmdPad_1().at(Transform((3.75, -4.35), 180)),
        33: RectSmdPad_1().at(Transform((4.35, -3.75), 270)),
        34: RectSmdPad_1().at(Transform((4.35, -3.25), 270)),
        35: RectSmdPad_1().at(Transform((4.35, -2.75), 270)),
        36: RectSmdPad_1().at(Transform((4.35, -2.25), 270)),
        37: RectSmdPad_1().at(Transform((4.35, -1.75), 270)),
        38: RectSmdPad_1().at(Transform((4.35, -1.25), 270)),
        39: RectSmdPad_1().at(Transform((4.35, -0.75), 270)),
        40: RectSmdPad_1().at(Transform((4.35, -0.25), 270)),
        41: RectSmdPad_1().at(Transform((4.35, 0.25), 270)),
        42: RectSmdPad_1().at(Transform((4.35, 0.75), 270)),
        43: RectSmdPad_1().at(Transform((4.35, 1.25), 270)),
        44: RectSmdPad_1().at(Transform((4.35, 1.75), 270)),
        45: RectSmdPad_1().at(Transform((4.35, 2.25), 270)),
        46: RectSmdPad_1().at(Transform((4.35, 2.75), 270)),
        47: RectSmdPad_1().at(Transform((4.35, 3.25), 270)),
        48: RectSmdPad_1().at(Transform((4.35, 3.75), 270)),
        49: RectSmdPad_1().at((3.75, 4.35)),
        50: RectSmdPad_1().at((3.25, 4.35)),
        51: RectSmdPad_1().at((2.75, 4.35)),
        52: RectSmdPad_1().at((2.25, 4.35)),
        53: RectSmdPad_1().at((1.75, 4.35)),
        54: RectSmdPad_1().at((1.25, 4.35)),
        55: RectSmdPad_1().at((0.75, 4.35)),
        56: RectSmdPad_1().at((0.25, 4.35)),
        57: RectSmdPad_1().at((-0.25, 4.35)),
        58: RectSmdPad_1().at((-0.75, 4.35)),
        59: RectSmdPad_1().at((-1.25, 4.35)),
        60: RectSmdPad_1().at((-1.75, 4.35)),
        61: RectSmdPad_1().at((-2.25, 4.35)),
        62: RectSmdPad_1().at((-2.75, 4.35)),
        63: RectSmdPad_1().at((-3.25, 4.35)),
        64: RectSmdPad_1().at((-3.75, 4.35)),
    }
    PAD = RectSmdPad_2().at((0, 0))

    silkscreen = [
        Silkscreen(Polyline(0.127, [(4.5, 4.5), (4, 4.5)])),
        Silkscreen(Polyline(0.127, [(-4, 4.5), (-4.5, 4.5)])),
        Silkscreen(Polyline(0.127, [(-4.5, 4.5), (-4.5, 4)])),
        Silkscreen(Polyline(0.127, [(4.5, 4), (4.5, 4.5)])),
        Silkscreen(Polyline(0.127, [(-4.5, -4), (-4.5, -4.5)])),
        Silkscreen(Polyline(0.127, [(4.5, -4.5), (4.5, -4)])),
        Silkscreen(Polyline(0.127, [(4, -4.5), (4.5, -4.5)])),
        Silkscreen(Polyline(0.127, [(-4.5, -4.5), (-4, -4.5)])),
        Silkscreen(ArcPolyline(0.3, [
            Arc((-5.25, 3.75), 0.15, 0, 360)])),
    ]

    # Model3D file not found: "${KIPRJMOD}/pcbgolf.3dshapes/Package_DFN_QFN.3dshapes/QFN-64-1EP_9x9mm_P0.5mm_EP4.1x4.1mm.step"


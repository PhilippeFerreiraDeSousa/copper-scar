# File Location: .local/small-loop/jitx/small_loop/imports/SmallLoop/landpatterns/LandpatternXTAL_3_2X2_5.py 
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


class RectSmdPad(Pad):
    shape = rectangle(1.3, 1.1)
    paste = [
        Paste(rectangle(1.3, 1.1)),
    ]
    soldermask = [
        Soldermask(rectangle(1.3, 1.1)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class LandpatternXTAL_3_2X2_5(Landpattern):
    p = {
        1: RectSmdPad().at((-1.15, -0.85)),
        2: RectSmdPad().at((1.15, -0.85)),
        3: RectSmdPad().at((1.15, 0.85)),
        4: RectSmdPad().at((-1.15, 0.85)),
    }

    silkscreen = [
        Silkscreen(Polyline(0.127, [(1.65, 1.25), (-1.55, 1.25)])),
        Silkscreen(Polyline(0.127, [(-1.55, 1.25), (-1.55, -1.25)])),
        Silkscreen(Polyline(0.127, [(1.65, -1.25), (1.65, 1.25)])),
        Silkscreen(Polyline(0.127, [(-1.55, -1.25), (1.65, -1.25)])),
        Silkscreen(ArcPolyline(0.127, [
            Arc((-2.05, -1.45), 0.1, 0, 360)])),
    ]

    # Model3D file not found: "${KIPRJMOD}/pcbgolf.3dshapes/Crystal.3dshapes/Crystal_SMD_3225-4Pin_3.2x2.5mm.step"


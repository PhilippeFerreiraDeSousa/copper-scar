# File Location: .local/small-loop/jitx/small_loop/imports/SmallLoop/landpatterns/LandpatternEVQ_Q2.py 
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
    shape = rectangle(3.2, 1.2)
    paste = [
        Paste(rectangle(3.2, 1.2)),
    ]
    soldermask = [
        Soldermask(rectangle(3.2, 1.2)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class LandpatternEVQ_Q2(Landpattern):
    A = {
        0: RectSmdPad().at((-3.4, -2)),
        1: RectSmdPad().at((3.4, -2)),
    }
    B = {
        0: RectSmdPad().at((-3.4, 2)),
        1: RectSmdPad().at((3.4, 2)),
    }

    silkscreen = [
        Silkscreen(Polyline(0.127, [(-3.3, 3), (3.3, 3)])),
        Silkscreen(Polyline(0.127, [(-3.3, -3), (-3.3, 3)])),
        Silkscreen(Polyline(0.127, [(3.3, 3), (3.3, -3)])),
        Silkscreen(Polyline(0.127, [(3.3, -3), (-3.3, -3)])),
        Silkscreen(ArcPolyline(0.127, [
            Arc((0, 0), 1, 0, 360)])),
        Silkscreen(ArcPolyline(0.127, [
            Arc((0, 0), 1.5033, 0, 360)])),
    ]

    # Model3D file not found: "${KIPRJMOD}/pcbgolf.3dshapes/Button_Switch_SMD.3dshapes/EVQQ2-BFKPUY-03W.step"


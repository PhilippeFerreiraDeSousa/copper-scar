# File Location: .local/small-loop/jitx/small_loop/imports/SmallLoop/landpatterns/LandpatternCHOKE_3_2X2_5.py 
from jitx.landpattern import Landpattern, Pad
from jitx.model3d import Model3D
from jitx.feature import Silkscreen, Paste, Soldermask
from jitx.shapes.primitive import Polyline
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
    shape = rectangle(1.05, 1.05)
    paste = [
        Paste(rectangle(1.05, 1.05)),
    ]
    soldermask = [
        Soldermask(rectangle(1.05, 1.05)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class LandpatternCHOKE_3_2X2_5(Landpattern):
    p = {
        1: RectSmdPad().at((-1.5, 0.725)),
        2: RectSmdPad().at((-1.5, -0.725)),
        3: RectSmdPad().at((1.5, -0.725)),
        4: RectSmdPad().at((1.5, 0.725)),
    }

    silkscreen = [
        Silkscreen(Polyline(0.127, [(1.65, 1.3), (1.65, -1.3)])),
        Silkscreen(Polyline(0.127, [(-1.65, 1.3), (1.65, 1.3)])),
        Silkscreen(Polyline(0.127, [(1.65, -1.3), (-1.65, -1.3)])),
        Silkscreen(Polyline(0.127, [(-1.65, -1.3), (-1.65, 1.3)])),
    ]

    # Model3D file not found: "${KIPRJMOD}/pcbgolf.3dshapes/Inductor_SMD.3dshapes/ACT1210D-101-2P-TL00.step"


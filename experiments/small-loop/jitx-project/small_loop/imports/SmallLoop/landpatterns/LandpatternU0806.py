# File Location: .local/small-loop/jitx/small_loop/imports/SmallLoop/landpatterns/LandpatternU0806.py 
from jitx.landpattern import Landpattern, Pad
from jitx.model3d import Model3D
from jitx.feature import Silkscreen, Custom, Paste, Soldermask
from jitx.shapes.primitive import Polyline, Polygon
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
    shape = rectangle(0.55, 1.6)
    paste = [
        Paste(rectangle(0.55, 1.6)),
    ]
    soldermask = [
        Soldermask(rectangle(0.55, 1.6)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class LandpatternU0806(Landpattern):
    p = {
        1: RectSmdPad().at((-0.9, 0)),
        2: RectSmdPad().at((0.9, 0)),
    }

    customlayer = [
        Custom(Polygon([
            (-0.508, 0.635),
            (-1.016, 0.635),
            (-1.016, -0.635),
            (-0.508, -0.635)]), name="Fab"),
        Custom(Polygon([
            (0.508, -0.635),
            (1.016, -0.635),
            (1.016, 0.635),
            (0.508, 0.635)]), name="Fab"),
    ]
    silkscreen = [
        Silkscreen(Polyline(0.127, [(1.5, 1.054), (-1.5, 1.054)])),
        Silkscreen(Polyline(0.127, [(-1.5, 1.054), (-1.5, -1.054)])),
        Silkscreen(Polyline(0.127, [(1.5, -1.054), (1.5, 1.054)])),
        Silkscreen(Polyline(0.127, [(-1.5, -1.054), (1.5, -1.054)])),
    ]

    # Model3D file not found: "${KIPRJMOD}/pcbgolf.3dshapes/Inductor_SMD.3dshapes/L_Cenker_CKCS201610.step"


# File Location: .local/small-loop/jitx/small_loop/imports/SmallLoop/landpatterns/LandpatternDO_214AA_SMB_.py 
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
    shape = rectangle(2.159, 2.743)
    paste = [
        Paste(rectangle(2.159, 2.743)),
    ]
    soldermask = [
        Soldermask(rectangle(2.159, 2.743)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class LandpatternDO_214AA_SMB_(Landpattern):
    p = {
        1: RectSmdPad().at((-2.21, 0)),
        2: RectSmdPad().at((2.21, 0)),
    }

    silkscreen = [
        Silkscreen(Polyline(0.1524, [(-2.16, -1.78), (2.16, -1.78)])),
        Silkscreen(Polyline(0.1524, [(-2.16, 1.78), (2.16, 1.78)])),
        Silkscreen(ArcPolyline(0.3048, [
            Arc((-3.04, -2.07), 0.1, 0, 360)])),
    ]

    # Model3D file not found: "${KIPRJMOD}/pcbgolf.3dshapes/Diode_SMD.3dshapes/D_SMB.step"


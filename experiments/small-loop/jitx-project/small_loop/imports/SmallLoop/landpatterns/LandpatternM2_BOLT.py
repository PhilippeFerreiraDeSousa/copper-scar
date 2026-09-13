# File Location: .local/small-loop/jitx/small_loop/imports/SmallLoop/landpatterns/LandpatternM2_BOLT.py 
from jitx.landpattern import Landpattern, Pad
from jitx.feature import Cutout, Soldermask
from jitx.layerindex import Side
from jitx.shapes.primitive import Circle

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


class CircleThPad(Pad):
    shape = Circle(radius=2.1)
    cutout = [
        Cutout(Circle(radius=1)),
    ]
    soldermask = [
        Soldermask(Circle(radius=2.1)),
        Soldermask(Circle(radius=2.1), side=Side.Bottom),
    ]
    def __init__(self):
        self.solder = make_soldermask(self.shape, amount=0.0508, thruhole=True)

class LandpatternM2_BOLT(Landpattern):
    p = {
        0: CircleThPad().at((0, 0)),
    }


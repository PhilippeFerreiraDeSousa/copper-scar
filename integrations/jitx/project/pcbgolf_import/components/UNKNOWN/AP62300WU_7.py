# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/components/UNKNOWN/AP62300WU_7.py 
# To import this component:
#     from .components.UNKNOWN import AP62300WU_7
#     u1 = AP62300WU_7.AP62300WU_7()
from jitx.landpattern import Landpattern, Pad
from jitx.model3d import Model3D
from jitx.symbol import Symbol, Pin, Direction
from jitx.component import Component
from jitx.net import Port
from jitx.landpattern import PadMapping
from jitx.symbol import SymbolMapping
from jitx.feature import Silkscreen, Custom, Paste, Soldermask
from jitx.shapes.primitive import Polyline, Circle, Polygon
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
    shape = rectangle(0.6, 0.9)
    paste = [
        Paste(rectangle(0.6, 0.9)),
    ]
    soldermask = [
        Soldermask(rectangle(0.6, 0.9)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class LandpatternSOT23_6(Landpattern):
    p = {
        1: RectSmdPad().at((-0.95, -1.15)),
        2: RectSmdPad().at((0, -1.15)),
        3: RectSmdPad().at((0.95, -1.15)),
        4: RectSmdPad().at((0.95, 1.15)),
        5: RectSmdPad().at((0, 1.15)),
        6: RectSmdPad().at((-0.95, 1.15)),
    }

    customlayer = [
        Custom(Polyline(0.1524, [(-1.423, 0.781), (1.422, 0.781)]), name="Fab"),
        Custom(Polyline(0.1524, [(1.422, -0.781), (-1.423, -0.781)]), name="Fab"),
        Custom(Polygon([
            (0.7, 0.8),
            (1.2, 0.8),
            (1.2, 1.4),
            (0.7, 1.4)]), name="Fab"),
        Custom(Polygon([
            (-0.25, 0.8),
            (0.25, 0.8),
            (0.25, 1.4),
            (-0.25, 1.4)]), name="Fab"),
        Custom(Polygon([
            (-1.2, 0.8),
            (-0.7, 0.8),
            (-0.7, 1.4),
            (-1.2, 1.4)]), name="Fab"),
        Custom(Polygon([
            (0.7, -1.4),
            (1.2, -1.4),
            (1.2, -0.8),
            (0.7, -0.8)]), name="Fab"),
        Custom(Polygon([
            (-0.25, -1.4),
            (0.25, -1.4),
            (0.25, -0.8),
            (-0.25, -0.8)]), name="Fab"),
        Custom(Polygon([
            (-1.2, -1.4),
            (-0.7, -1.4),
            (-0.7, -0.8),
            (-1.2, -0.8)]), name="Fab"),
    ]
    silkscreen = [
        Silkscreen(Polyline(0.1524, [(1.422, 0.781), (1.422, -0.781)])),
        Silkscreen(Polyline(0.1524, [(-1.423, -0.781), (-1.423, 0.781)])),
        Silkscreen(Circle(radius=0.05).at(-1.15, -0.5)),
    ]

    models = [
        Model3D("SOT-23-6.step",
            position=(0, 0, 0),
            scale=(1, 1, 1),
            rotation=(0, 0, -90),
        ),
    ]

class Symbolcomma_ai_11112255_AP62300T(Symbol):
    pin_name_size = 1.2
    pad_name_size = 1.2
    GND = Pin((0, -6), 4, Direction.Down)
    SW = Pin((8, 2), 4, Direction.Right)
    IN = Pin((-8, 2), 4, Direction.Left)
    FB = Pin((8, -4), 4, Direction.Right)
    EN = Pin((-8, -4), 4, Direction.Left)
    BST = Pin((8, 0), 4, Direction.Right)
    draws = [
        Polyline(0.1524, [(-8, -6), (-8, 4)]),
        Polyline(0.1524, [(8, 4), (8, -6)]),
        Polyline(0.1524, [(-8, 4), (8, 4)]),
        Polyline(0.1524, [(8, -6), (-8, -6)]),
    ]

class AP62300WU_7(Component):
    description = ""
    mpn = "AP62300WU-7"
    datasheet = ""
    reference_designator_prefix = "U"
    landpattern = LandpatternSOT23_6()
    GND = Port()
    SW = Port()
    IN = Port()
    FB = Port()
    EN = Port()
    BST = Port()
    symbol = Symbolcomma_ai_11112255_AP62300T()
    mappings = [
        SymbolMapping({
            GND: symbol.GND, 
            SW: symbol.SW, 
            IN: symbol.IN, 
            FB: symbol.FB, 
            EN: symbol.EN, 
            BST: symbol.BST
        }),
        PadMapping({
            GND: landpattern.p[1],
            SW: landpattern.p[2],
            IN: landpattern.p[3],
            FB: landpattern.p[4],
            EN: landpattern.p[5],
            BST: landpattern.p[6],
        }),
    ]

Device: type[AP62300WU_7] = AP62300WU_7

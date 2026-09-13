# File Location: b-compatible-output/converted/imports/Pcbgolf/components/UNKNOWN/PJ_002AH_SMT_TR.py 
# To import this component:
#     from .components.UNKNOWN import PJ_002AH_SMT_TR
#     u1 = PJ_002AH_SMT_TR.PJ_002AH_SMT_TR()
from jitx.landpattern import Landpattern, Pad
from jitx.model3d import Model3D
from jitx.symbol import Symbol, Pin, Direction
from jitx.component import Component
from jitx.net import Port
from jitx.landpattern import PadMapping
from jitx.symbol import SymbolMapping
from jitx.feature import Silkscreen, Custom, Paste, KeepOut, Cutout, Soldermask
from jitx.layerindex import Side, LayerSet
from jitx.anchor import Anchor
from jitx.shapes.primitive import Polyline, Circle, Arc, ArcPolyline, Polygon, Text
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


class RectSmdPad(Pad):
    shape = rectangle(2.4, 2)
    paste = [
        Paste(rectangle(2.4, 2)),
    ]
    soldermask = [
        Soldermask(rectangle(2.4, 2)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class LandpatternDCJACK_2MM_SMT(Landpattern):
    GND = RectSmdPad().at((0, -5.5))
    GNDBREAK = RectSmdPad().at((6.2, -5.5))
    PWR1 = RectSmdPad().at((0, 5.5))
    PWR2 = RectSmdPad().at((6.2, 5.5))

    customlayer = [
        Custom(Polyline(0.127, [(-5, 3.5), (-5, -3.5)]), name="Fab"),
        Custom(Polyline(0.127, [(-4, -4.5), (10.254, -4.5)]), name="Fab"),
        Custom(Polyline(0.127, [(9, 4.5), (-4, 4.5)]), name="Fab"),
        Custom(Polyline(0.127, [(9, -1.492), (9, 4.5)]), name="Fab"),
        Custom(Polyline(0.127, [(10.254, -1.492), (9, -1.492)]), name="Fab"),
        Custom(Polyline(0.127, [(10.254, -4.5), (10.254, -1.492)]), name="Fab"),
        Custom(ArcPolyline(0.127, [
            Arc((-4, 3.5), 1, 180.00004, -90.00009)]), name="Fab"),
        Custom(ArcPolyline(0.127, [
            Arc((-4, -3.5), 1, 270.00004, -90.00009)]), name="Fab"),
    ]
    silkscreen = [
        Silkscreen(Polyline(0.127, [(-5, 3.5), (-5, -3.5)])),
        Silkscreen(Polyline(0.127, [(-4, -4.5), (-1.684, -4.5)])),
        Silkscreen(Polyline(0.127, [(-1.668, 4.5), (-4, 4.5)])),
        Silkscreen(Polyline(0.127, [(1.588, -4.5), (4.666, -4.5)])),
        Silkscreen(Polyline(0.127, [(4.682, 4.5), (1.588, 4.5)])),
        Silkscreen(Polyline(0.127, [(7.938, -4.5), (10.254, -4.5)])),
        Silkscreen(Polyline(0.127, [(9, 4.5), (7.938, 4.5)])),
        Silkscreen(Polyline(0.127, [(9, -1.492), (9, 4.5)])),
        Silkscreen(Polyline(0.127, [(10.254, -1.492), (9, -1.492)])),
        Silkscreen(Polyline(0.127, [(10.254, -4.5), (10.254, -1.492)])),
        Silkscreen(ArcPolyline(0.127, [
            Arc((-4, 3.5), 1, 180.00004, -90.00009)])),
        Silkscreen(ArcPolyline(0.127, [
            Arc((-4, -3.5), 1, 270.00004, -90.00009)])),
        Silkscreen(Text("GND", 0.74778, Anchor.C).at((-1.016, -3.81))),
        Silkscreen(Text("+", 1.25171, Anchor.C).at(Transform((0.762, 2.794), 90))),
    ]
    forbidvia = [
        KeepOut(Polygon([
            (-6.4262, -4.445),
            (-5.9436, -4.445),
            (-5.9436, -4.4196),
            (-6.4262, -4.4196)]), layers=LayerSet((0, -1)), via=True),
        KeepOut(Polygon([
            (-4.9022, -5.7404),
            (-4.9022, -5.2578),
            (-4.9276, -5.2578),
            (-4.9276, -5.7404)]), layers=LayerSet((0, -1)), via=True),
        KeepOut(Polygon([
            (-1.27, -5.7404),
            (-1.27, -5.2578),
            (-1.2954, -5.2578),
            (-1.2954, -5.7404)]), layers=LayerSet((0, -1)), via=True),
        KeepOut(Polygon([
            (0.254, -4.4196),
            (-0.2286, -4.4196),
            (-0.2286, -4.445),
            (0.254, -4.445)]), layers=LayerSet((0, -1)), via=True),
    ]
    cutout = [
        Cutout(Circle(radius=0.8)),
        Cutout(Circle(radius=0.9).at(4.5, 0)),
    ]
    soldermask = [
        Soldermask(Circle(radius=0.8)),
        Soldermask(Circle(radius=0.8), side=Side.Bottom),
        Soldermask(Circle(radius=0.9).at(4.5, 0)),
        Soldermask(Circle(radius=0.9).at(4.5, 0), side=Side.Bottom),
    ]
    forbidcopper = [
        KeepOut(Polygon([
            (-6.4262, -4.445),
            (-5.9436, -4.445),
            (-5.9436, -4.4196),
            (-6.4262, -4.4196)]), layers=LayerSet((0, 0)), pour=True, route=True),
        KeepOut(Polygon([
            (-4.9022, -5.7404),
            (-4.9022, -5.2578),
            (-4.9276, -5.2578),
            (-4.9276, -5.7404)]), layers=LayerSet((0, 0)), pour=True, route=True),
        KeepOut(Polygon([
            (-1.27, -5.7404),
            (-1.27, -5.2578),
            (-1.2954, -5.2578),
            (-1.2954, -5.7404)]), layers=LayerSet((0, 0)), pour=True, route=True),
        KeepOut(Polygon([
            (0.254, -4.4196),
            (-0.2286, -4.4196),
            (-0.2286, -4.445),
            (0.254, -4.445)]), layers=LayerSet((0, 0)), pour=True, route=True),
    ]

    models = [
        Model3D("PJ-002AH-SMT-TR.step",
            position=(-5, 0, 6.5),
            scale=(1, 1, 1),
            rotation=(-90, 0, 90),
        ),
    ]

class Symbolcomma_ai_11112255_DCBARRELSMT(Symbol):
    pin_name_size = 0
    pad_name_size = 1.2
    GNDBREAK = Pin((0, 0), 2, Direction.Right)
    GND = Pin((0, -2), 2, Direction.Right)
    PWR = Pin((0, 2), 2, Direction.Right)
    draws = [
        Text(">REF", 0.85, Anchor.W).at((-4, 4)),
        Text(">VALUE", 0.85, Anchor.W).at((-4, -4)),
        Text("pcbgolf:DCJACK_2MM_SMT", 1, Anchor.C),
        Text("", 1, Anchor.C),
        Polyline(0.254, [(0, 1.5), (-3.5, 1.5)]),
        Polyline(0.1524, [(0, 0), (0, -2)]),
        Polyline(0.254, [(0, 2.5), (0, 1.5)]),
        Polyline(0.254, [(0, 2.5), (-3.5, 2.5)]),
        Polyline(0.254, [(-2, -1), (-1, -2)]),
        Polyline(0.254, [(-3, -2), (-2, -1)]),
        ArcPolyline(0.254, [
            Arc((-3.5, 2), 0.5, 270, -180)]),
        Polyline(0.254, [(-4, -2), (-3, -2)]),
        Polyline(0.254, [(0, -2), (-1, -2)]),
    ]
    if False : # hidden objects
        draw_hidden = Text("ki_locked: ", 1, Anchor.C)

class PJ_002AH_SMT_TR(Component):
    description = ""
    mpn = "PJ-002AH-SMT-TR"
    datasheet = ""
    reference_designator_prefix = "J1"
    landpattern = LandpatternDCJACK_2MM_SMT()
    GNDBREAK = Port()
    GND = Port()
    PWR = Port()
    symbol = Symbolcomma_ai_11112255_DCBARRELSMT()
    mappings = [
        SymbolMapping({
            GNDBREAK: symbol.GNDBREAK, 
            GND: symbol.GND, 
            PWR: symbol.PWR
        }),
        PadMapping({
            GNDBREAK: landpattern.GND,
            GND: landpattern.GNDBREAK,
            PWR: landpattern.PWR1,
        }),
    ]

Device: type[PJ_002AH_SMT_TR] = PJ_002AH_SMT_TR

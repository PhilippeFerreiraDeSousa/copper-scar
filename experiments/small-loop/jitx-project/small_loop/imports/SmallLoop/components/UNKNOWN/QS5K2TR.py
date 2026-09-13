# File Location: .local/small-loop/jitx/small_loop/imports/SmallLoop/components/UNKNOWN/QS5K2TR.py 
# To import this component:
#     from .components.UNKNOWN import QS5K2TR
#     u1 = QS5K2TR.QS5K2TR()
from jitx.landpattern import Landpattern, Pad
from jitx.model3d import Model3D
from jitx.symbol import Symbol, Pin, Direction
from jitx.component import Component
from jitx.net import Port
from jitx.landpattern import PadMapping
from jitx.symbol import SymbolMapping
from jitx.feature import Silkscreen, Custom, Paste, Soldermask
from jitx.anchor import Anchor
from jitx.shapes.primitive import Polyline, Circle, Polygon, Text
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
    shape = rectangle(0.55, 1.2)
    paste = [
        Paste(rectangle(0.55, 1.2)),
    ]
    soldermask = [
        Soldermask(rectangle(0.55, 1.2)),
    ]
    def __init__(self):
        self.paste = make_pastemask(self.shape, amount=0)
        self.solder = make_soldermask(self.shape, amount=0.0508)

class LandpatternSOT23_5(Landpattern):
    p = {
        1: RectSmdPad().at((-0.95, -1.3001)),
        2: RectSmdPad().at((0, -1.3001)),
        3: RectSmdPad().at((0.95, -1.3001)),
        4: RectSmdPad().at((0.95, 1.3001)),
        5: RectSmdPad().at((-0.95, 1.3001)),
    }

    customlayer = [
        Custom(Polyline(0.1524, [(-1.4, 0.8), (-1.4, -0.8)]), name="Fab"),
        Custom(Polyline(0.1524, [(-1.4, 0.8), (1.4, 0.8)]), name="Fab"),
        Custom(Polyline(0.1524, [(1.4, 0.8), (1.4, -0.8)]), name="Fab"),
        Custom(Polyline(0.1524, [(1.4, -0.8), (-1.4, -0.8)]), name="Fab"),
        Custom(Polygon([
            (-1.2, 0.85),
            (-0.7, 0.85),
            (-0.7, 1.5),
            (-1.2, 1.5)]), name="Fab"),
        Custom(Polygon([
            (-1.2, -1.5),
            (-0.7, -1.5),
            (-0.7, -0.85),
            (-1.2, -0.85)]), name="Fab"),
        Custom(Polygon([
            (-0.25, -1.5),
            (0.25, -1.5),
            (0.25, -0.85),
            (-0.25, -0.85)]), name="Fab"),
        Custom(Polygon([
            (0.7, 0.85),
            (1.2, 0.85),
            (1.2, 1.5),
            (0.7, 1.5)]), name="Fab"),
        Custom(Polygon([
            (0.7, -1.5),
            (1.2, -1.5),
            (1.2, -0.85),
            (0.7, -0.85)]), name="Fab"),
    ]
    silkscreen = [
        Silkscreen(Polyline(0.2032, [(-1.4224, -0.4294), (-1.4224, 0.4294)])),
        Silkscreen(Polyline(0.2032, [(-0.2684, 0.8104), (0.2684, 0.8104)])),
        Silkscreen(Polyline(0.2032, [(1.4224, 0.4294), (1.4224, -0.4294)])),
    ]

    # Model3D file not found: "${KIPRJMOD}/pcbgolf.3dshapes/Package_TO_SOT_SMD.3dshapes/SOT-23-5.step"

class Symbolcomma_ai_11112255_NFET_DUAL_COMMON_SOURCE_QS5K2(Symbol):
    pin_name_size = 0
    pad_name_size = 0
    G1 = Pin((-4, 0), 2, Direction.Left)
    S = Pin((4, -4), 2, Direction.Down)
    G2 = Pin((12, 0), 2, Direction.Right)
    D2 = Pin((8, 2), 2, Direction.Up)
    D1 = Pin((0, 2), 2, Direction.Up)
    draws = [
        Text(">REF", 1.19, Anchor.W).at((0, 6.29921)),
        Text(">VALUE", 1, Anchor.C).at((0, 4.72441)),
        Text("pcbgolf:SOT23-5", 1, Anchor.C).at((0, 3.14961)),
        Text("", 1, Anchor.C).at((0, 1.5748)),
        Polyline(0.1524, [(1.5, -0.5), (2.5, -0.5)]),
        Polyline(0.1524, [(8, 2), (8, 1.5)]),
        Polyline(0.3048, [(-1.4, 0), (-0.7, 0.2)]),
        Polyline(0.1524, [(5.5, 0.6), (5.3, 0.8)]),
        Polyline(0.1524, [(2, 0.6), (2, 1.5)]),
        Polyline(0.1524, [(2.5, 0.6), (2.7, 0.8)]),
        Polyline(0.254, [(10.88, 1.9), (10.88, -2)]),
        Polyline(0.1524, [(0, -1.5), (0, -2)]),
        Polyline(0.1524, [(8.6, 0), (8, 0)]),
        Polyline(0.1524, [(8.6, 0), (8.6, -0.4)]),
        Polyline(0.1524, [(0, 1.5), (2, 1.5)]),
        Polyline(0.3048, [(8.7, -0.2), (9.4, 0)]),
        Polyline(0.254, [(0, -4), (8, -4)]),
        Polyline(0.1524, [(0, 2), (0, 1.5)]),
        Polyline(0.1524, [(-0.6, 0), (0, 0)]),
        Polyline(0.1524, [(2.5, -0.5), (2, 0.6)]),
        Polyline(0.1524, [(-0.6, -0.4), (-1.6, 0)]),
        Polyline(0.254, [(0, -2), (0, -4)]),
        Polyline(0.1524, [(2, -1.5), (0, -1.5)]),
        Transform((9.9, 0)) * rectangle(0.6, 1.4),
        Polyline(0.1524, [(-0.6, 0), (-0.6, -0.4)]),
        Polyline(0.3048, [(-0.7, 0.2), (-0.7, 0)]),
        Polyline(0.1524, [(2, -1.5), (2, 0.6)]),
        Polyline(0.1524, [(-0.6, 0.4), (-0.6, 0)]),
        Polyline(0.1524, [(9.6, -1.5), (8, -1.5)]),
        Polyline(0.1524, [(0, 1.5), (-1.58, 1.5)]),
        Polyline(0.1524, [(8.6, 0.4), (8.6, 0)]),
        Polyline(0.1524, [(6.5, -0.5), (5.5, -0.5)]),
        Polyline(0.1524, [(1.5, 0.6), (1.3, 0.4)]),
        Polyline(0.254, [(-2.88, 1.9), (-2.88, -2)]),
        Polyline(0.1524, [(-3, 0), (-4, 0)]),
        Polyline(0.1524, [(6.5, 0.6), (6, 0.6)]),
        Polyline(0.1524, [(8.7, 0), (9.6, 0)]),
        Polyline(0.1524, [(6.5, 0.6), (6.7, 0.4)]),
        Polyline(0.1524, [(8, -1.5), (8, -2)]),
        Polyline(0.1524, [(6, 0.6), (6, 1.5)]),
        Polyline(0.1524, [(-0.7, 0), (-1.6, 0)]),
        Polyline(0.3048, [(-0.7, 0), (-0.9, 0)]),
        Polyline(0.1524, [(9.6, 0), (8.6, 0.4)]),
        Polyline(0.1524, [(6, 0.6), (6.5, -0.5)]),
        Polyline(0.1524, [(8, 0), (8, -1.5)]),
        Polyline(0.1524, [(2, 0.6), (1.5, -0.5)]),
        Polyline(0.1524, [(2, 0.6), (2.5, 0.6)]),
        Polyline(0.1524, [(6, -1.5), (8, -1.5)]),
        Polyline(0.1524, [(8.6, -0.4), (9.6, 0)]),
        Polyline(0.1524, [(-1.6, 0), (-0.6, 0.4)]),
        Polyline(0.1524, [(5.5, -0.5), (6, 0.6)]),
        Polyline(0.1524, [(6, -1.5), (6, 0.6)]),
        Polyline(0.1524, [(8, 1.5), (9.58, 1.5)]),
        Polyline(0.1524, [(8, 1.5), (6, 1.5)]),
        Polyline(0.1524, [(-1.6, -1.5), (0, -1.5)]),
        Polyline(0.254, [(8, -4), (8, -2)]),
        Polyline(0.3048, [(8.7, 0.2), (8.7, 0)]),
        Polyline(0.3048, [(9.4, 0), (8.7, 0.2)]),
        Polyline(0.1524, [(1.5, 0.6), (2, 0.6)]),
        Polyline(0.1524, [(0, 0), (0, -1.5)]),
        Transform((-1.9, 0)) * rectangle(0.6, 1.4),
        Transform((9.9, -1.5)) * rectangle(0.6, 1),
        Transform((9.9, 1.5)) * rectangle(0.6, 1),
        Transform((-1.9, 1.5)) * rectangle(0.6, 1),
        Transform((-1.9, -1.5)) * rectangle(0.6, 1),
        Circle(radius=0.1).at(0, -1.5),
        Circle(radius=0.1).at(8, 1.5),
        Circle(radius=0.1).at(0, 1.5),
        Circle(radius=0.1).at(8, -1.5),
        Polyline(0.1524, [(6, 0.6), (5.5, 0.6)]),
        Polyline(0.3048, [(-0.7, -0.2), (-1.4, 0)]),
        Polyline(0.3048, [(8.7, 0), (8.9, 0)]),
        Polyline(0.1524, [(11, 0), (12, 0)]),
        Text("S", 0.54394, Anchor.W).at((-1, -2.8)),
        Text("D", 0.54394, Anchor.E).at((9, 2)),
        Text("D", 0.54394, Anchor.W).at((-1, 2)),
        Text("G", 0.54394, Anchor.W).at((-4, -1)),
        Text("G", 0.54394, Anchor.E).at((12, -1)),
        Text("S", 0.54394, Anchor.E).at((9, -2.8)),
    ]
    if False : # hidden objects
        draw_hidden = Text("ki_locked: ", 1, Anchor.C)

class QS5K2TR(Component):
    description = ""
    mpn = "QS5K2TR"
    datasheet = ""
    reference_designator_prefix = "Q2"
    landpattern = LandpatternSOT23_5()
    G1 = Port()
    S = Port()
    G2 = Port()
    D2 = Port()
    D1 = Port()
    symbol = Symbolcomma_ai_11112255_NFET_DUAL_COMMON_SOURCE_QS5K2()
    mappings = [
        SymbolMapping({
            G1: symbol.G1, 
            S: symbol.S, 
            G2: symbol.G2, 
            D2: symbol.D2, 
            D1: symbol.D1
        }),
        PadMapping({
            G1: landpattern.p[1],
            S: landpattern.p[2],
            G2: landpattern.p[3],
            D2: landpattern.p[4],
            D1: landpattern.p[5],
        }),
    ]

Device: type[QS5K2TR] = QS5K2TR

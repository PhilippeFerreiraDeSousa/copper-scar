# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/components/UNKNOWN/USB2517.py 
# To import this component:
#     from .components.UNKNOWN import USB2517
#     u1 = USB2517.USB2517()
from jitx.landpattern import Landpattern, Pad
from jitx.model3d import Model3D
from jitx.symbol import Symbol, Pin, Direction
from jitx.component import Component
from jitx.net import Port
from jitx.landpattern import PadMapping
from jitx.symbol import SymbolMapping
from jitx.feature import Silkscreen, Paste, Soldermask
from jitx.anchor import Anchor
from jitx.shapes.primitive import Polyline, Arc, ArcPolyline, Text
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

    models = [
        Model3D("QFN-64-1EP_9x9mm_P0.5mm_EP4.1x4.1mm.step",
            position=(0, 0, 0),
            scale=(1, 1, 1),
            rotation=(0, 0, 0),
        ),
    ]

class Symbolcomma_ai_11112255_USB2517(Symbol):
    pin_name_size = 1.2
    pad_name_size = 1.2
    USBDN1_DM = Pin((30, 94), 4, Direction.Right)
    USBDN1_DP = Pin((30, 96), 4, Direction.Right)
    USBDN2_DM = Pin((30, 80), 4, Direction.Right)
    USBDN2_DP = Pin((30, 82), 4, Direction.Right)
    USBDN3_DM = Pin((30, 66), 4, Direction.Right)
    USBDN3_DP = Pin((30, 68), 4, Direction.Right)
    USBDN4_DM = Pin((30, 52), 4, Direction.Right)
    USBDN4_DP = Pin((30, 54), 4, Direction.Right)
    USBDN5_DM = Pin((30, 38), 4, Direction.Right)
    USBDN5_DP = Pin((30, 40), 4, Direction.Right)
    CFG_SEL2 = Pin((0, 6), 4, Direction.Left)
    LED_B7_N = Pin((30, 6), 4, Direction.Right)
    LED_A7_N = Pin((30, 8), 4, Direction.Right)
    LED_B6_N = Pin((30, 20), 4, Direction.Right)
    LED_A6_N = Pin((30, 22), 4, Direction.Right)
    LED_B5_N = Pin((30, 34), 4, Direction.Right)
    TEST = Pin((0, 24), 4, Direction.Left)
    PRTPWR4 = Pin((30, 46), 4, Direction.Right)
    OCS4_N = Pin((30, 44), 4, Direction.Right)
    OCS3_N = Pin((30, 58), 4, Direction.Right)
    PRTPWR3 = Pin((30, 60), 4, Direction.Right)
    VDD33CR = Pin((0, 92), 4, Direction.Left)
    VDD18 = Pin((0, 82), 4, Direction.Left)
    PRTPWR2 = Pin((30, 74), 4, Direction.Right)
    OCS2_N = Pin((30, 72), 4, Direction.Right)
    OCS1_N = Pin((30, 86), 4, Direction.Right)
    PRTPWR1 = Pin((30, 88), 4, Direction.Right)
    PRTPWR5 = Pin((30, 32), 4, Direction.Right)
    LED_A5_N = Pin((30, 36), 4, Direction.Right)
    LED_B4_N = Pin((30, 48), 4, Direction.Right)
    LED_A4_N = Pin((30, 50), 4, Direction.Right)
    LED_B3_N = Pin((30, 62), 4, Direction.Right)
    OCS5_N = Pin((30, 30), 4, Direction.Right)
    PRTPWR7 = Pin((30, 4), 4, Direction.Right)
    OCS7_N = Pin((30, 2), 4, Direction.Right)
    OCS6_N = Pin((30, 16), 4, Direction.Right)
    PRTPWR6 = Pin((30, 18), 4, Direction.Right)
    SDA = Pin((0, 32), 4, Direction.Left)
    SCL = Pin((0, 30), 4, Direction.Left)
    CFG_SEL1 = Pin((0, 8), 4, Direction.Left)
    RESET_N = Pin((0, 86), 4, Direction.Left)
    VBUS_DET = Pin((0, 76), 4, Direction.Left)
    SUSP_IND = Pin((0, 22), 4, Direction.Left)
    VDD33 = Pin((0, 96), 4, Direction.Left)
    LED_A3_N = Pin((30, 64), 4, Direction.Right)
    LED_B2_N = Pin((30, 76), 4, Direction.Right)
    LED_A2_N = Pin((30, 78), 4, Direction.Right)
    LED_B1_N = Pin((30, 90), 4, Direction.Right)
    LED_A1_N = Pin((30, 92), 4, Direction.Right)
    USBDN6_DM = Pin((30, 24), 4, Direction.Right)
    USBDN6_DP = Pin((30, 26), 4, Direction.Right)
    USBDN7_DM = Pin((30, 10), 4, Direction.Right)
    USBDN7_DP = Pin((30, 12), 4, Direction.Right)
    VDDA33 = Pin((0, 94), 4, Direction.Left, pin_name_size=0)
    USBUP_DM = Pin((0, 70), 4, Direction.Left)
    USBUP_DP = Pin((0, 72), 4, Direction.Left)
    XTAL2 = Pin((0, 16), 4, Direction.Left)
    XTAL1 = Pin((0, 18), 4, Direction.Left)
    VDD18PLL = Pin((0, 80), 4, Direction.Left)
    RBIAS = Pin((0, 12), 4, Direction.Left)
    VDD33PLL = Pin((0, 90), 4, Direction.Left)
    VSS = Pin((0, 2), 4, Direction.Left)
    draws = [
        Text(">REF", 0.85, Anchor.W).at((0, -2)),
        Text(">VALUE", 1, Anchor.C),
        Text("pcbgolf:QFN64-9X9", 1, Anchor.C),
        Text("", 1, Anchor.C),
        Polyline(0.254, [(0, 0), (30, 0)]),
        Polyline(0.254, [(30, 98), (0, 98)]),
        Polyline(0.254, [(0, 98), (0, 0)]),
        Polyline(0.254, [(30, 0), (30, 98)]),
    ]
    if False : # hidden objects
        draw_hidden = Text("ki_locked: ", 1, Anchor.C)

class USB2517(Component):
    description = ""
    mpn = "USB2517"
    datasheet = ""
    reference_designator_prefix = "U4"
    landpattern = LandpatternQFN64_9X9()
    USBDN1_DM = Port()
    USBDN1_DP = Port()
    USBDN2_DM = Port()
    USBDN2_DP = Port()
    USBDN3_DM = Port()
    USBDN3_DP = Port()
    USBDN4_DM = Port()
    USBDN4_DP = Port()
    USBDN5_DM = Port()
    USBDN5_DP = Port()
    CFG_SEL2 = Port()
    LED_B7_N = Port()
    LED_A7_N = Port()
    LED_B6_N = Port()
    LED_A6_N = Port()
    LED_B5_N = Port()
    TEST = Port()
    PRTPWR4 = Port()
    OCS4_N = Port()
    OCS3_N = Port()
    PRTPWR3 = Port()
    VDD33CR = Port()
    VDD18 = Port()
    PRTPWR2 = Port()
    OCS2_N = Port()
    OCS1_N = Port()
    PRTPWR1 = Port()
    PRTPWR5 = Port()
    LED_A5_N = Port()
    LED_B4_N = Port()
    LED_A4_N = Port()
    LED_B3_N = Port()
    OCS5_N = Port()
    PRTPWR7 = Port()
    OCS7_N = Port()
    OCS6_N = Port()
    PRTPWR6 = Port()
    SDA = Port()
    SCL = Port()
    CFG_SEL1 = Port()
    RESET_N = Port()
    VBUS_DET = Port()
    SUSP_IND = Port()
    VDD33 = Port()
    LED_A3_N = Port()
    LED_B2_N = Port()
    LED_A2_N = Port()
    LED_B1_N = Port()
    LED_A1_N = Port()
    USBDN6_DM = Port()
    USBDN6_DP = Port()
    USBDN7_DM = Port()
    USBDN7_DP = Port()
    VDDA33 = Port()
    USBUP_DM = Port()
    USBUP_DP = Port()
    XTAL2 = Port()
    XTAL1 = Port()
    VDD18PLL = Port()
    RBIAS = Port()
    VDD33PLL = Port()
    VSS = Port()
    symbol = Symbolcomma_ai_11112255_USB2517()
    mappings = [
        SymbolMapping({
            USBDN1_DM: symbol.USBDN1_DM, 
            USBDN1_DP: symbol.USBDN1_DP, 
            USBDN2_DM: symbol.USBDN2_DM, 
            USBDN2_DP: symbol.USBDN2_DP, 
            USBDN3_DM: symbol.USBDN3_DM, 
            USBDN3_DP: symbol.USBDN3_DP, 
            USBDN4_DM: symbol.USBDN4_DM, 
            USBDN4_DP: symbol.USBDN4_DP, 
            USBDN5_DM: symbol.USBDN5_DM, 
            USBDN5_DP: symbol.USBDN5_DP, 
            CFG_SEL2: symbol.CFG_SEL2, 
            LED_B7_N: symbol.LED_B7_N, 
            LED_A7_N: symbol.LED_A7_N, 
            LED_B6_N: symbol.LED_B6_N, 
            LED_A6_N: symbol.LED_A6_N, 
            LED_B5_N: symbol.LED_B5_N, 
            TEST: symbol.TEST, 
            PRTPWR4: symbol.PRTPWR4, 
            OCS4_N: symbol.OCS4_N, 
            OCS3_N: symbol.OCS3_N, 
            PRTPWR3: symbol.PRTPWR3, 
            VDD33CR: symbol.VDD33CR, 
            VDD18: symbol.VDD18, 
            PRTPWR2: symbol.PRTPWR2, 
            OCS2_N: symbol.OCS2_N, 
            OCS1_N: symbol.OCS1_N, 
            PRTPWR1: symbol.PRTPWR1, 
            PRTPWR5: symbol.PRTPWR5, 
            LED_A5_N: symbol.LED_A5_N, 
            LED_B4_N: symbol.LED_B4_N, 
            LED_A4_N: symbol.LED_A4_N, 
            LED_B3_N: symbol.LED_B3_N, 
            OCS5_N: symbol.OCS5_N, 
            PRTPWR7: symbol.PRTPWR7, 
            OCS7_N: symbol.OCS7_N, 
            OCS6_N: symbol.OCS6_N, 
            PRTPWR6: symbol.PRTPWR6, 
            SDA: symbol.SDA, 
            SCL: symbol.SCL, 
            CFG_SEL1: symbol.CFG_SEL1, 
            RESET_N: symbol.RESET_N, 
            VBUS_DET: symbol.VBUS_DET, 
            SUSP_IND: symbol.SUSP_IND, 
            VDD33: symbol.VDD33, 
            LED_A3_N: symbol.LED_A3_N, 
            LED_B2_N: symbol.LED_B2_N, 
            LED_A2_N: symbol.LED_A2_N, 
            LED_B1_N: symbol.LED_B1_N, 
            LED_A1_N: symbol.LED_A1_N, 
            USBDN6_DM: symbol.USBDN6_DM, 
            USBDN6_DP: symbol.USBDN6_DP, 
            USBDN7_DM: symbol.USBDN7_DM, 
            USBDN7_DP: symbol.USBDN7_DP, 
            VDDA33: symbol.VDDA33, 
            USBUP_DM: symbol.USBUP_DM, 
            USBUP_DP: symbol.USBUP_DP, 
            XTAL2: symbol.XTAL2, 
            XTAL1: symbol.XTAL1, 
            VDD18PLL: symbol.VDD18PLL, 
            RBIAS: symbol.RBIAS, 
            VDD33PLL: symbol.VDD33PLL, 
            VSS: symbol.VSS
        }),
        PadMapping({
            USBDN1_DM: landpattern.p[1],
            USBDN1_DP: landpattern.p[2],
            USBDN2_DM: landpattern.p[3],
            USBDN2_DP: landpattern.p[4],
            USBDN3_DM: landpattern.p[6],
            USBDN3_DP: landpattern.p[7],
            USBDN4_DM: landpattern.p[8],
            USBDN4_DP: landpattern.p[9],
            USBDN5_DM: landpattern.p[11],
            USBDN5_DP: landpattern.p[12],
            CFG_SEL2: landpattern.p[13],
            LED_B7_N: landpattern.p[14],
            LED_A7_N: landpattern.p[15],
            LED_B6_N: landpattern.p[16],
            LED_A6_N: landpattern.p[17],
            LED_B5_N: landpattern.p[18],
            TEST: landpattern.p[19],
            PRTPWR4: landpattern.p[20],
            OCS4_N: landpattern.p[21],
            OCS3_N: landpattern.p[22],
            PRTPWR3: landpattern.p[23],
            VDD33CR: landpattern.p[24],
            VDD18: landpattern.p[25],
            PRTPWR2: landpattern.p[26],
            OCS2_N: landpattern.p[27],
            OCS1_N: landpattern.p[28],
            PRTPWR1: landpattern.p[29],
            PRTPWR5: landpattern.p[30],
            LED_A5_N: landpattern.p[31],
            LED_B4_N: landpattern.p[32],
            LED_A4_N: landpattern.p[33],
            LED_B3_N: landpattern.p[34],
            OCS5_N: landpattern.p[35],
            PRTPWR7: landpattern.p[36],
            OCS7_N: landpattern.p[37],
            OCS6_N: landpattern.p[38],
            PRTPWR6: landpattern.p[39],
            SDA: landpattern.p[40],
            SCL: landpattern.p[41],
            CFG_SEL1: landpattern.p[42],
            RESET_N: landpattern.p[43],
            VBUS_DET: landpattern.p[44],
            SUSP_IND: landpattern.p[45],
            VDD33: landpattern.p[46],
            LED_A3_N: landpattern.p[47],
            LED_B2_N: landpattern.p[48],
            LED_A2_N: landpattern.p[49],
            LED_B1_N: landpattern.p[50],
            LED_A1_N: landpattern.p[51],
            USBDN6_DM: landpattern.p[53],
            USBDN6_DP: landpattern.p[54],
            USBDN7_DM: landpattern.p[55],
            USBDN7_DP: landpattern.p[56],
            VDDA33: [
                landpattern.p[57],
                landpattern.p[52],
                landpattern.p[10],
                landpattern.p[5],
            ],
            USBUP_DM: landpattern.p[58],
            USBUP_DP: landpattern.p[59],
            XTAL2: landpattern.p[60],
            XTAL1: landpattern.p[61],
            VDD18PLL: landpattern.p[62],
            RBIAS: landpattern.p[63],
            VDD33PLL: landpattern.p[64],
            VSS: landpattern.PAD,
        }),
    ]

Device: type[USB2517] = USB2517

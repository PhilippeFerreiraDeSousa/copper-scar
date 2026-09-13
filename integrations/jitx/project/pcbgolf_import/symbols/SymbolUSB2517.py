# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/symbols/SymbolUSB2517.py 
from jitx.symbol import Symbol, Pin, Direction
from jitx.shapes.primitive import Polyline


class SymbolUSB2517(Symbol):
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
        Polyline(0.254, [(0, 0), (30, 0)]),
        Polyline(0.254, [(30, 98), (0, 98)]),
        Polyline(0.254, [(0, 98), (0, 0)]),
        Polyline(0.254, [(30, 0), (30, 98)]),
    ]


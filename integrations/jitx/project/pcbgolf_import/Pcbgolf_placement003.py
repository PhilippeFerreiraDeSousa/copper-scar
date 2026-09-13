# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/Pcbgolf.py 
from jitx.circuit import Circuit
from jitx.net import Port, Net
from jitx.transform import Transform


from .components.UNKNOWN import LG_R971_KN_1_4 as LG_R971_KN_1
from .components.UNKNOWN import RC0402FR_0710KL as RC0402FR_0710KL
from .components.UNKNOWN import RC0402JR_07100KL as RC0402JR_07100KL
from .components.UNKNOWN import RC0402JR_072K7L as RC0402JR_072K7L
from .components.UNKNOWN import NCS20071SN2T1G as NCS20071SN2T1G
from .symbols.SymbolU_5V_1 import SymbolU_5V
from .symbols.SymbolU_12V_2 import SymbolU_12V
class Pcbgolf_4_01(Circuit):
    CAN3_H_1 = Port()
    CAN3_L_1 = Port()
    GND_1 = Port()
    U_12V = Port()
    U_5V = Port()

    LED5 = LG_R971_KN_1.Device()
    R59 = RC0402FR_0710KL.Device()
    R60 = RC0402FR_0710KL.Device()
    R61 = RC0402JR_07100KL.Device()
    R65 = RC0402JR_072K7L.Device()
    U12 = NCS20071SN2T1G.Device()

    nets = [
        Net([LED5.A, R65.p[2]], name="Net_LED5_PadA"),
        Net([R65.p[1], U12.p[1]], name="Net_R65_Pad1"),
        Net([R59.p[2], U12.p[0]], name="Net_U12_"),
        Net([R60.p[2], R61.p[1], U12.n], name="Net_U12__"),
        Net([CAN3_H_1, R59.p[1]], name="CAN3_H"),
        Net([CAN3_L_1, R60.p[1]], name="CAN3_L"),
        Net([GND_1, LED5.C, U12.Vn], name="GND"),
        Net([U_12V, U12.Vp], name="Net12V", symbol=SymbolU_12V()),
        Net([U_5V, R61.p[2]], name="Net5V", symbol=SymbolU_5V()),
    ]

    def __init__(self):
        self.place(self.LED5, Transform((39.1553, 0)))
        self.place(self.R59, Transform((0, 15.534)))
        self.place(self.R60, Transform((0, 13.507)))
        self.place(self.R61, Transform((0, 11.48)))
        self.place(self.R65, Transform((0, 3.372)))
        self.place(self.U12, Transform((17.7058, 9.6485)))



from .components.UNKNOWN import LG_R971_KN_1_2 as LG_R971_KN_1
from .components.UNKNOWN import RC0402FR_0710KL as RC0402FR_0710KL
from .components.UNKNOWN import RC0402JR_07100KL as RC0402JR_07100KL
from .components.UNKNOWN import RC0402JR_072K7L as RC0402JR_072K7L
from .components.UNKNOWN import NCS20071SN2T1G as NCS20071SN2T1G
from .symbols.SymbolU_5V_1 import SymbolU_5V
from .symbols.SymbolU_12V_2 import SymbolU_12V
class Pcbgolf_4_02(Circuit):
    CAN2_H_1 = Port()
    CAN2_L_1 = Port()
    GND_1 = Port()
    U_12V = Port()
    U_5V = Port()

    LED4 = LG_R971_KN_1.Device()
    R56 = RC0402FR_0710KL.Device()
    R57 = RC0402FR_0710KL.Device()
    R58 = RC0402JR_07100KL.Device()
    R64 = RC0402JR_072K7L.Device()
    U11 = NCS20071SN2T1G.Device()

    nets = [
        Net([LED4.A, R64.p[2]], name="Net_LED4_PadA"),
        Net([R64.p[1], U11.p[1]], name="Net_R64_Pad1"),
        Net([R56.p[2], U11.p[0]], name="Net_U11_"),
        Net([R57.p[2], R58.p[1], U11.n], name="Net_U11__"),
        Net([CAN2_H_1, R56.p[1]], name="CAN2_H"),
        Net([CAN2_L_1, R57.p[1]], name="CAN2_L"),
        Net([GND_1, LED4.C, U11.Vn], name="GND"),
        Net([U_12V, U11.Vp], name="Net12V", symbol=SymbolU_12V()),
        Net([U_5V, R58.p[2]], name="Net5V", symbol=SymbolU_5V()),
    ]

    def __init__(self):
        self.place(self.LED4, Transform((36.6283, 0)))
        self.place(self.R56, Transform((0, 21.615)))
        self.place(self.R57, Transform((0, 19.588)))
        self.place(self.R58, Transform((0, 17.561)))
        self.place(self.R64, Transform((0, 5.399)))
        self.place(self.U11, Transform((17.7058, 16.2335)))



from .components.UNKNOWN import LG_R971_KN_1_1 as LG_R971_KN_1
from .components.UNKNOWN import RC0402FR_0710KL as RC0402FR_0710KL
from .components.UNKNOWN import RC0402JR_07100KL as RC0402JR_07100KL
from .components.UNKNOWN import RC0402JR_072K7L as RC0402JR_072K7L
from .components.UNKNOWN import NCS20071SN2T1G as NCS20071SN2T1G
from .symbols.SymbolU_5V_1 import SymbolU_5V
from .symbols.SymbolU_12V_2 import SymbolU_12V
class Pcbgolf_4_03(Circuit):
    CAN1_H_1 = Port()
    CAN1_L_1 = Port()
    GND_1 = Port()
    U_12V = Port()
    U_5V = Port()

    LED3 = LG_R971_KN_1.Device()
    R53 = RC0402FR_0710KL.Device()
    R54 = RC0402FR_0710KL.Device()
    R55 = RC0402JR_07100KL.Device()
    R63 = RC0402JR_072K7L.Device()
    U10 = NCS20071SN2T1G.Device()

    nets = [
        Net([LED3.A, R63.p[2]], name="Net_LED3_PadA"),
        Net([R63.p[1], U10.p[1]], name="Net_R63_Pad1"),
        Net([R53.p[2], U10.p[0]], name="Net_U10_"),
        Net([R54.p[2], R55.p[1], U10.n], name="Net_U10__"),
        Net([CAN1_H_1, R53.p[1]], name="CAN1_H"),
        Net([CAN1_L_1, R54.p[1]], name="CAN1_L"),
        Net([GND_1, LED3.C, U10.Vn], name="GND"),
        Net([U_12V, U10.Vp], name="Net12V", symbol=SymbolU_12V()),
        Net([U_5V, R55.p[2]], name="Net5V", symbol=SymbolU_5V()),
    ]

    def __init__(self):
        self.place(self.LED3, Transform((34.1013, 0)))
        self.place(self.R53, Transform((0, 27.696)))
        self.place(self.R54, Transform((0, 25.669)))
        self.place(self.R55, Transform((0, 23.642)))
        self.place(self.R63, Transform((0, 7.426)))
        self.place(self.U10, Transform((17.7058, 22.8185)))



from .components.UNKNOWN import CL05F104ZO5NNNC as CL05F104ZO5NNNC
from .symbols.SymbolU_12V_2 import SymbolU_12V
class Pcbgolf_4_04(Circuit):
    GND_1 = Port()
    U_12V = Port()

    C49 = CL05F104ZO5NNNC.Device()

    nets = [
        Net([GND_1, C49.p[2]], name="GND"),
        Net([U_12V, C49.p[1]], name="Net12V", symbol=SymbolU_12V()),
    ]

    def __init__(self):
        self.place(self.C49, Transform((0, 0)))



from .components.UNKNOWN import CL05F104ZO5NNNC as CL05F104ZO5NNNC
from .symbols.SymbolU_12V_2 import SymbolU_12V
class Pcbgolf_4_05(Circuit):
    GND_1 = Port()
    U_12V = Port()

    C48 = CL05F104ZO5NNNC.Device()

    nets = [
        Net([GND_1, C48.p[2]], name="GND"),
        Net([U_12V, C48.p[1]], name="Net12V", symbol=SymbolU_12V()),
    ]

    def __init__(self):
        self.place(self.C48, Transform((0, 0)))



from .components.UNKNOWN import CL05F104ZO5NNNC as CL05F104ZO5NNNC
from .symbols.SymbolU_12V_2 import SymbolU_12V
class Pcbgolf_4_06(Circuit):
    GND_1 = Port()
    U_12V = Port()

    C47 = CL05F104ZO5NNNC.Device()

    nets = [
        Net([GND_1, C47.p[2]], name="GND"),
        Net([U_12V, C47.p[1]], name="Net12V", symbol=SymbolU_12V()),
    ]

    def __init__(self):
        self.place(self.C47, Transform((0, 0)))



from .components.UNKNOWN import CL05F104ZO5NNNC as CL05F104ZO5NNNC
from .symbols.SymbolU_12V_2 import SymbolU_12V
class Pcbgolf_4_07(Circuit):
    GND_1 = Port()
    U_12V = Port()

    C46 = CL05F104ZO5NNNC.Device()

    nets = [
        Net([GND_1, C46.p[2]], name="GND"),
        Net([U_12V, C46.p[1]], name="Net12V", symbol=SymbolU_12V()),
    ]

    def __init__(self):
        self.place(self.C46, Transform((0, 0)))



from .components.UNKNOWN import CL05F104ZO5NNNC as CL05F104ZO5NNNC
from .symbols.SymbolU_3V3_2 import SymbolU_3V3
class Pcbgolf_4_08(Circuit):
    GND_1 = Port()
    U_3V3 = Port()

    C45 = CL05F104ZO5NNNC.Device()

    nets = [
        Net([GND_1, C45.p[2]], name="GND"),
        Net([U_3V3, C45.p[1]], name="Net3V3", symbol=SymbolU_3V3()),
    ]

    def __init__(self):
        self.place(self.C45, Transform((0, 0)))



from .components.UNKNOWN import CL05F104ZO5NNNC as CL05F104ZO5NNNC
from .symbols.SymbolU_3V3_2 import SymbolU_3V3
class Pcbgolf_4_09(Circuit):
    GND_1 = Port()
    U_3V3 = Port()

    C44 = CL05F104ZO5NNNC.Device()

    nets = [
        Net([GND_1, C44.p[2]], name="GND"),
        Net([U_3V3, C44.p[1]], name="Net3V3", symbol=SymbolU_3V3()),
    ]

    def __init__(self):
        self.place(self.C44, Transform((0, 0)))



from .components.UNKNOWN import CL05F104ZO5NNNC as CL05F104ZO5NNNC
from .symbols.SymbolU_3V3_2 import SymbolU_3V3
class Pcbgolf_4_10(Circuit):
    GND_1 = Port()
    U_3V3 = Port()

    C43 = CL05F104ZO5NNNC.Device()

    nets = [
        Net([GND_1, C43.p[2]], name="GND"),
        Net([U_3V3, C43.p[1]], name="Net3V3", symbol=SymbolU_3V3()),
    ]

    def __init__(self):
        self.place(self.C43, Transform((0, 0)))



from .components.UNKNOWN import CL05F104ZO5NNNC as CL05F104ZO5NNNC
from .symbols.SymbolU_3V3_2 import SymbolU_3V3
class Pcbgolf_4_11(Circuit):
    GND_1 = Port()
    U_3V3 = Port()

    C42 = CL05F104ZO5NNNC.Device()

    nets = [
        Net([GND_1, C42.p[2]], name="GND"),
        Net([U_3V3, C42.p[1]], name="Net3V3", symbol=SymbolU_3V3()),
    ]

    def __init__(self):
        self.place(self.C42, Transform((0, 0)))



from .components.UNKNOWN import CL05F104ZO5NNNC as CL05F104ZO5NNNC
from .symbols.SymbolU_5V_1 import SymbolU_5V
class Pcbgolf_4_12(Circuit):
    GND_1 = Port()
    U_5V = Port()

    C41 = CL05F104ZO5NNNC.Device()

    nets = [
        Net([GND_1, C41.p[2]], name="GND"),
        Net([U_5V, C41.p[1]], name="Net5V", symbol=SymbolU_5V()),
    ]

    def __init__(self):
        self.place(self.C41, Transform((0, 0)))



from .components.UNKNOWN import CL05F104ZO5NNNC as CL05F104ZO5NNNC
from .symbols.SymbolU_5V_1 import SymbolU_5V
class Pcbgolf_4_13(Circuit):
    GND_1 = Port()
    U_5V = Port()

    C40 = CL05F104ZO5NNNC.Device()

    nets = [
        Net([GND_1, C40.p[2]], name="GND"),
        Net([U_5V, C40.p[1]], name="Net5V", symbol=SymbolU_5V()),
    ]

    def __init__(self):
        self.place(self.C40, Transform((0, 0)))



from .components.UNKNOWN import CL05F104ZO5NNNC as CL05F104ZO5NNNC
from .symbols.SymbolU_5V_1 import SymbolU_5V
class Pcbgolf_4_14(Circuit):
    GND_1 = Port()
    U_5V = Port()

    C39 = CL05F104ZO5NNNC.Device()

    nets = [
        Net([GND_1, C39.p[2]], name="GND"),
        Net([U_5V, C39.p[1]], name="Net5V", symbol=SymbolU_5V()),
    ]

    def __init__(self):
        self.place(self.C39, Transform((0, 0)))



from .components.UNKNOWN import CL05F104ZO5NNNC as CL05F104ZO5NNNC
from .symbols.SymbolU_5V_1 import SymbolU_5V
class Pcbgolf_4_15(Circuit):
    GND_1 = Port()
    U_5V = Port()

    C38 = CL05F104ZO5NNNC.Device()

    nets = [
        Net([GND_1, C38.p[2]], name="GND"),
        Net([U_5V, C38.p[1]], name="Net5V", symbol=SymbolU_5V()),
    ]

    def __init__(self):
        self.place(self.C38, Transform((0, 0)))



from .components.UNKNOWN import comma_ai_11112255_M2X4 as comma_ai_11112255_M2X4
class Pcbgolf_4_16(Circuit):
    CAN0_H_1 = Port()
    CAN0_L_1 = Port()
    CAN1_H_1 = Port()
    CAN1_L_1 = Port()
    CAN2_H_1 = Port()
    CAN2_L_1 = Port()
    CAN3_H_1 = Port()
    CAN3_L_1 = Port()

    J4 = comma_ai_11112255_M2X4.Device()

    nets = [
        Net([CAN0_H_1, J4.p[2]], name="CAN0_H"),
        Net([CAN0_L_1, J4.p[1]], name="CAN0_L"),
        Net([CAN1_H_1, J4.p[4]], name="CAN1_H"),
        Net([CAN1_L_1, J4.p[3]], name="CAN1_L"),
        Net([CAN2_H_1, J4.p[6]], name="CAN2_H"),
        Net([CAN2_L_1, J4.p[5]], name="CAN2_L"),
        Net([CAN3_H_1, J4.p[8]], name="CAN3_H"),
        Net([CAN3_L_1, J4.p[7]], name="CAN3_L"),
    ]

    def __init__(self):
        self.place(self.J4, Transform((0, 0)))

        self.J4.x_out = True


from .components.UNKNOWN import ACT1210D_101_2P_TL00 as ACT1210D_101_2P_TL00
from .components.UNKNOWN import MCP2542FDT_H_MNY as MCP2542FDT_H_MNY
from .symbols.SymbolU_3V3_2 import SymbolU_3V3
from .symbols.SymbolU_5V_1 import SymbolU_5V
class Pcbgolf_4_17(Circuit):
    CAN3_EN_1 = Port()
    CAN3_H_1 = Port()
    CAN3_L_1 = Port()
    CAN3_RX_1 = Port()
    CAN3_TX_1 = Port()
    GND_1 = Port()
    U_3V3 = Port()
    U_5V = Port()

    L8 = ACT1210D_101_2P_TL00.Device()
    U8 = MCP2542FDT_H_MNY.Device()

    nets = [
        Net([L8.p[1], U8.CANH], name="Net_U8_CANH"),
        Net([L8.p[2], U8.CANL], name="Net_U8_CANL"),
        Net([CAN3_EN_1, U8.STBY], name="CAN3_EN"),
        Net([CAN3_H_1, L8.p[4]], name="CAN3_H"),
        Net([CAN3_L_1, L8.p[3]], name="CAN3_L"),
        Net([CAN3_RX_1, U8.RXD], name="CAN3_RX"),
        Net([CAN3_TX_1, U8.TXD], name="CAN3_TX"),
        Net([GND_1, U8.EPAD, U8.VSS], name="GND"),
        Net([U_3V3, U8.VIO], name="Net3V3", symbol=SymbolU_3V3()),
        Net([U_5V, U8.VDD], name="Net5V", symbol=SymbolU_5V()),
    ]

    def __init__(self):
        self.place(self.L8, Transform((0, 0)))
        self.place(self.U8, Transform((38.8636, 37.4791)))



from .components.UNKNOWN import ACT1210D_101_2P_TL00 as ACT1210D_101_2P_TL00
from .components.UNKNOWN import MCP2542FDT_H_MNY as MCP2542FDT_H_MNY
from .symbols.SymbolU_3V3_2 import SymbolU_3V3
from .symbols.SymbolU_5V_1 import SymbolU_5V
class Pcbgolf_4_18(Circuit):
    CAN2_EN_1 = Port()
    CAN2_H_1 = Port()
    CAN2_L_1 = Port()
    CAN2_RX_1 = Port()
    CAN2_TX_1 = Port()
    GND_1 = Port()
    U_3V3 = Port()
    U_5V = Port()

    L7 = ACT1210D_101_2P_TL00.Device()
    U7 = MCP2542FDT_H_MNY.Device()

    nets = [
        Net([L7.p[1], U7.CANH], name="Net_U7_CANH"),
        Net([L7.p[2], U7.CANL], name="Net_U7_CANL"),
        Net([CAN2_EN_1, U7.STBY], name="CAN2_EN"),
        Net([CAN2_H_1, L7.p[4]], name="CAN2_H"),
        Net([CAN2_L_1, L7.p[3]], name="CAN2_L"),
        Net([CAN2_RX_1, U7.RXD], name="CAN2_RX"),
        Net([CAN2_TX_1, U7.TXD], name="CAN2_TX"),
        Net([GND_1, U7.EPAD, U7.VSS], name="GND"),
        Net([U_3V3, U7.VIO], name="Net3V3", symbol=SymbolU_3V3()),
        Net([U_5V, U7.VDD], name="Net5V", symbol=SymbolU_5V()),
    ]

    def __init__(self):
        self.place(self.L7, Transform((0, 0)))
        self.place(self.U7, Transform((38.8636, 36.9365)))



from .components.UNKNOWN import ACT1210D_101_2P_TL00 as ACT1210D_101_2P_TL00
from .components.UNKNOWN import MCP2542FDT_H_MNY as MCP2542FDT_H_MNY
from .symbols.SymbolU_3V3_2 import SymbolU_3V3
from .symbols.SymbolU_5V_1 import SymbolU_5V
class Pcbgolf_4_19(Circuit):
    CAN1_EN_1 = Port()
    CAN1_H_1 = Port()
    CAN1_L_1 = Port()
    CAN1_RX_1 = Port()
    CAN1_TX_1 = Port()
    GND_1 = Port()
    U_3V3 = Port()
    U_5V = Port()

    L6 = ACT1210D_101_2P_TL00.Device()
    U6 = MCP2542FDT_H_MNY.Device()

    nets = [
        Net([L6.p[1], U6.CANH], name="Net_U6_CANH"),
        Net([L6.p[2], U6.CANL], name="Net_U6_CANL"),
        Net([CAN1_EN_1, U6.STBY], name="CAN1_EN"),
        Net([CAN1_H_1, L6.p[4]], name="CAN1_H"),
        Net([CAN1_L_1, L6.p[3]], name="CAN1_L"),
        Net([CAN1_RX_1, U6.RXD], name="CAN1_RX"),
        Net([CAN1_TX_1, U6.TXD], name="CAN1_TX"),
        Net([GND_1, U6.EPAD, U6.VSS], name="GND"),
        Net([U_3V3, U6.VIO], name="Net3V3", symbol=SymbolU_3V3()),
        Net([U_5V, U6.VDD], name="Net5V", symbol=SymbolU_5V()),
    ]

    def __init__(self):
        self.place(self.L6, Transform((0, 0)))
        self.place(self.U6, Transform((38.8636, 36.3939)))



from .components.UNKNOWN import ACT1210D_101_2P_TL00 as ACT1210D_101_2P_TL00
from .components.UNKNOWN import MCP2542FDT_H_MNY as MCP2542FDT_H_MNY
from .symbols.SymbolU_5V_1 import SymbolU_5V
from .symbols.SymbolU_3V3_2 import SymbolU_3V3
class Pcbgolf_4_20(Circuit):
    CAN0_EN_1 = Port()
    CAN0_H_1 = Port()
    CAN0_L_1 = Port()
    CAN0_RX_1 = Port()
    CAN0_TX_1 = Port()
    GND_1 = Port()
    U_3V3 = Port()
    U_5V = Port()

    L5 = ACT1210D_101_2P_TL00.Device()
    U5 = MCP2542FDT_H_MNY.Device()

    nets = [
        Net([L5.p[1], U5.CANH], name="Net_U5_CANH"),
        Net([L5.p[2], U5.CANL], name="Net_U5_CANL"),
        Net([CAN0_EN_1, U5.STBY], name="CAN0_EN"),
        Net([CAN0_H_1, L5.p[4]], name="CAN0_H"),
        Net([CAN0_L_1, L5.p[3]], name="CAN0_L"),
        Net([CAN0_RX_1, U5.RXD], name="CAN0_RX"),
        Net([CAN0_TX_1, U5.TXD], name="CAN0_TX"),
        Net([GND_1, U5.EPAD, U5.VSS], name="GND"),
        Net([U_3V3, U5.VIO], name="Net3V3", symbol=SymbolU_3V3()),
        Net([U_5V, U5.VDD], name="Net5V", symbol=SymbolU_5V()),
    ]

    def __init__(self):
        self.place(self.L5, Transform((0, 0)))
        self.place(self.U5, Transform((38.8636, 35.8513)))



from .components.UNKNOWN import LG_R971_KN_1_3 as LG_R971_KN_1
from .components.UNKNOWN import RC0402FR_0710KL as RC0402FR_0710KL
from .components.UNKNOWN import RC0402JR_07100KL as RC0402JR_07100KL
from .components.UNKNOWN import RC0402JR_072K7L as RC0402JR_072K7L
from .components.UNKNOWN import NCS20071SN2T1G as NCS20071SN2T1G
from .symbols.SymbolU_12V_2 import SymbolU_12V
from .symbols.SymbolU_5V_1 import SymbolU_5V
class Pcbgolf_4_21(Circuit):
    CAN0_H_1 = Port()
    CAN0_L_1 = Port()
    GND_1 = Port()
    U_12V = Port()
    U_5V = Port()

    LED2 = LG_R971_KN_1.Device()
    R50 = RC0402FR_0710KL.Device()
    R51 = RC0402FR_0710KL.Device()
    R52 = RC0402JR_07100KL.Device()
    R62 = RC0402JR_072K7L.Device()
    U9 = NCS20071SN2T1G.Device()

    nets = [
        Net([LED2.A, R62.p[2]], name="Net_LED2_PadA"),
        Net([R62.p[1], U9.p[1]], name="Net_R62_Pad1"),
        Net([R50.p[2], U9.p[0]], name="Net_U9_"),
        Net([R51.p[2], R52.p[1], U9.n], name="Net_U9__"),
        Net([CAN0_H_1, R50.p[1]], name="CAN0_H"),
        Net([CAN0_L_1, R51.p[1]], name="CAN0_L"),
        Net([GND_1, LED2.C, U9.Vn], name="GND"),
        Net([U_12V, U9.Vp], name="Net12V", symbol=SymbolU_12V()),
        Net([U_5V, R52.p[2]], name="Net5V", symbol=SymbolU_5V()),
    ]

    def __init__(self):
        self.place(self.LED2, Transform((34.5711, 0)))
        self.place(self.R50, Transform((0, 3.372)))
        self.place(self.R51, Transform((2.9968, 31.75)))
        self.place(self.R52, Transform((2.9968, 29.723)))
        self.place(self.R62, Transform((2.9968, 9.453)))
        self.place(self.U9, Transform((20.7026, 29.4035)))



from .components.UNKNOWN import RC0402FR_0760R4L as RC0402FR_0760R4L
class Pcbgolf_4_22(Circuit):
    CAN3_H_1 = Port()
    CAN3_L_1 = Port()

    R49 = RC0402FR_0760R4L.Device()

    nets = [
        Net([CAN3_H_1, R49.p[2]], name="CAN3_H"),
        Net([CAN3_L_1, R49.p[1]], name="CAN3_L"),
    ]

    def __init__(self):
        self.place(self.R49, Transform((0, 0)))



from .components.UNKNOWN import RC0402FR_0760R4L as RC0402FR_0760R4L
class Pcbgolf_4_23(Circuit):
    CAN2_H_1 = Port()
    CAN2_L_1 = Port()

    R48 = RC0402FR_0760R4L.Device()

    nets = [
        Net([CAN2_H_1, R48.p[2]], name="CAN2_H"),
        Net([CAN2_L_1, R48.p[1]], name="CAN2_L"),
    ]

    def __init__(self):
        self.place(self.R48, Transform((0, 0)))



from .components.UNKNOWN import RC0402FR_0760R4L as RC0402FR_0760R4L
class Pcbgolf_4_24(Circuit):
    CAN1_H_1 = Port()
    CAN1_L_1 = Port()

    R47 = RC0402FR_0760R4L.Device()

    nets = [
        Net([CAN1_H_1, R47.p[2]], name="CAN1_H"),
        Net([CAN1_L_1, R47.p[1]], name="CAN1_L"),
    ]

    def __init__(self):
        self.place(self.R47, Transform((0, 0)))



from .components.UNKNOWN import RC0402FR_0760R4L as RC0402FR_0760R4L
class Pcbgolf_4_25(Circuit):
    CAN0_H_1 = Port()
    CAN0_L_1 = Port()

    R46 = RC0402FR_0760R4L.Device()

    nets = [
        Net([CAN0_H_1, R46.p[2]], name="CAN0_H"),
        Net([CAN0_L_1, R46.p[1]], name="CAN0_L"),
    ]

    def __init__(self):
        self.place(self.R46, Transform((0, 0)))



from .symbols.SymbolU_5V_1 import SymbolU_5V
from .symbols.SymbolU_12V_2 import SymbolU_12V
from .symbols.SymbolU_3V3_2 import SymbolU_3V3
class Pcbgolf_4(Circuit):
    CAN0_EN_1 = Port()
    CAN0_H_1 = Port()
    CAN0_L_1 = Port()
    CAN0_RX_1 = Port()
    CAN0_TX_1 = Port()
    CAN1_EN_1 = Port()
    CAN1_H_1 = Port()
    CAN1_L_1 = Port()
    CAN1_RX_1 = Port()
    CAN1_TX_1 = Port()
    CAN2_EN_1 = Port()
    CAN2_H_1 = Port()
    CAN2_L_1 = Port()
    CAN2_RX_1 = Port()
    CAN2_TX_1 = Port()
    CAN3_EN_1 = Port()
    CAN3_H_1 = Port()
    CAN3_L_1 = Port()
    CAN3_RX_1 = Port()
    CAN3_TX_1 = Port()
    GND_1 = Port()
    U_12V = Port()
    U_3V3 = Port()
    U_5V = Port()

    Pcbgolf_4_01 = Pcbgolf_4_01()
    Pcbgolf_4_02 = Pcbgolf_4_02()
    Pcbgolf_4_03 = Pcbgolf_4_03()
    Pcbgolf_4_04 = Pcbgolf_4_04()
    Pcbgolf_4_05 = Pcbgolf_4_05()
    Pcbgolf_4_06 = Pcbgolf_4_06()
    Pcbgolf_4_07 = Pcbgolf_4_07()
    Pcbgolf_4_08 = Pcbgolf_4_08()
    Pcbgolf_4_09 = Pcbgolf_4_09()
    Pcbgolf_4_10 = Pcbgolf_4_10()
    Pcbgolf_4_11 = Pcbgolf_4_11()
    Pcbgolf_4_12 = Pcbgolf_4_12()
    Pcbgolf_4_13 = Pcbgolf_4_13()
    Pcbgolf_4_14 = Pcbgolf_4_14()
    Pcbgolf_4_15 = Pcbgolf_4_15()
    Pcbgolf_4_16 = Pcbgolf_4_16()
    Pcbgolf_4_17 = Pcbgolf_4_17()
    Pcbgolf_4_18 = Pcbgolf_4_18()
    Pcbgolf_4_19 = Pcbgolf_4_19()
    Pcbgolf_4_20 = Pcbgolf_4_20()
    Pcbgolf_4_21 = Pcbgolf_4_21()
    Pcbgolf_4_22 = Pcbgolf_4_22()
    Pcbgolf_4_23 = Pcbgolf_4_23()
    Pcbgolf_4_24 = Pcbgolf_4_24()
    Pcbgolf_4_25 = Pcbgolf_4_25()

    nets = [
        Net([CAN0_EN_1, Pcbgolf_4_20.CAN0_EN_1], name="CAN0_EN"),
        Net([CAN0_H_1, Pcbgolf_4_16.CAN0_H_1, Pcbgolf_4_20.CAN0_H_1, Pcbgolf_4_21.CAN0_H_1, Pcbgolf_4_25.CAN0_H_1], name="CAN0_H"),
        Net([CAN0_L_1, Pcbgolf_4_16.CAN0_L_1, Pcbgolf_4_20.CAN0_L_1, Pcbgolf_4_21.CAN0_L_1, Pcbgolf_4_25.CAN0_L_1], name="CAN0_L"),
        Net([CAN0_RX_1, Pcbgolf_4_20.CAN0_RX_1], name="CAN0_RX"),
        Net([CAN0_TX_1, Pcbgolf_4_20.CAN0_TX_1], name="CAN0_TX"),
        Net([CAN1_EN_1, Pcbgolf_4_19.CAN1_EN_1], name="CAN1_EN"),
        Net([CAN1_H_1, Pcbgolf_4_03.CAN1_H_1, Pcbgolf_4_16.CAN1_H_1, Pcbgolf_4_19.CAN1_H_1, Pcbgolf_4_24.CAN1_H_1], name="CAN1_H"),
        Net([CAN1_L_1, Pcbgolf_4_03.CAN1_L_1, Pcbgolf_4_16.CAN1_L_1, Pcbgolf_4_19.CAN1_L_1, Pcbgolf_4_24.CAN1_L_1], name="CAN1_L"),
        Net([CAN1_RX_1, Pcbgolf_4_19.CAN1_RX_1], name="CAN1_RX"),
        Net([CAN1_TX_1, Pcbgolf_4_19.CAN1_TX_1], name="CAN1_TX"),
        Net([CAN2_EN_1, Pcbgolf_4_18.CAN2_EN_1], name="CAN2_EN"),
        Net([CAN2_H_1, Pcbgolf_4_02.CAN2_H_1, Pcbgolf_4_16.CAN2_H_1, Pcbgolf_4_18.CAN2_H_1, Pcbgolf_4_23.CAN2_H_1], name="CAN2_H"),
        Net([CAN2_L_1, Pcbgolf_4_02.CAN2_L_1, Pcbgolf_4_16.CAN2_L_1, Pcbgolf_4_18.CAN2_L_1, Pcbgolf_4_23.CAN2_L_1], name="CAN2_L"),
        Net([CAN2_RX_1, Pcbgolf_4_18.CAN2_RX_1], name="CAN2_RX"),
        Net([CAN2_TX_1, Pcbgolf_4_18.CAN2_TX_1], name="CAN2_TX"),
        Net([CAN3_EN_1, Pcbgolf_4_17.CAN3_EN_1], name="CAN3_EN"),
        Net([CAN3_H_1, Pcbgolf_4_01.CAN3_H_1, Pcbgolf_4_16.CAN3_H_1, Pcbgolf_4_17.CAN3_H_1, Pcbgolf_4_22.CAN3_H_1], name="CAN3_H"),
        Net([CAN3_L_1, Pcbgolf_4_01.CAN3_L_1, Pcbgolf_4_16.CAN3_L_1, Pcbgolf_4_17.CAN3_L_1, Pcbgolf_4_22.CAN3_L_1], name="CAN3_L"),
        Net([CAN3_RX_1, Pcbgolf_4_17.CAN3_RX_1], name="CAN3_RX"),
        Net([CAN3_TX_1, Pcbgolf_4_17.CAN3_TX_1], name="CAN3_TX"),
        Net([GND_1, Pcbgolf_4_01.GND_1, Pcbgolf_4_02.GND_1, Pcbgolf_4_03.GND_1, Pcbgolf_4_04.GND_1, Pcbgolf_4_05.GND_1, Pcbgolf_4_06.GND_1, Pcbgolf_4_07.GND_1, Pcbgolf_4_08.GND_1, Pcbgolf_4_09.GND_1, Pcbgolf_4_10.GND_1, Pcbgolf_4_11.GND_1, Pcbgolf_4_12.GND_1, Pcbgolf_4_13.GND_1, Pcbgolf_4_14.GND_1, Pcbgolf_4_15.GND_1, Pcbgolf_4_17.GND_1, Pcbgolf_4_18.GND_1, Pcbgolf_4_19.GND_1, Pcbgolf_4_20.GND_1, Pcbgolf_4_21.GND_1], name="GND"),
        Net([U_12V, Pcbgolf_4_01.U_12V, Pcbgolf_4_02.U_12V, Pcbgolf_4_03.U_12V, Pcbgolf_4_04.U_12V, Pcbgolf_4_05.U_12V, Pcbgolf_4_06.U_12V, Pcbgolf_4_07.U_12V, Pcbgolf_4_21.U_12V], name="Net12V", symbol=SymbolU_12V()),
        Net([U_3V3, Pcbgolf_4_08.U_3V3, Pcbgolf_4_09.U_3V3, Pcbgolf_4_10.U_3V3, Pcbgolf_4_11.U_3V3, Pcbgolf_4_17.U_3V3, Pcbgolf_4_18.U_3V3, Pcbgolf_4_19.U_3V3, Pcbgolf_4_20.U_3V3], name="Net3V3", symbol=SymbolU_3V3()),
        Net([U_5V, Pcbgolf_4_01.U_5V, Pcbgolf_4_02.U_5V, Pcbgolf_4_03.U_5V, Pcbgolf_4_12.U_5V, Pcbgolf_4_13.U_5V, Pcbgolf_4_14.U_5V, Pcbgolf_4_15.U_5V, Pcbgolf_4_17.U_5V, Pcbgolf_4_18.U_5V, Pcbgolf_4_19.U_5V, Pcbgolf_4_20.U_5V, Pcbgolf_4_21.U_5V], name="Net5V", symbol=SymbolU_5V()),
    ]

    def __init__(self):
        self.place(self.Pcbgolf_4_01, Transform((14.984, 31.481)))
        self.place(self.Pcbgolf_4_02, Transform((14.984, 31.481)))
        self.place(self.Pcbgolf_4_03, Transform((14.984, 31.481)))
        self.place(self.Pcbgolf_4_04, Transform((2.9968, 44.988)))
        self.place(self.Pcbgolf_4_05, Transform((2.9968, 47.015)))
        self.place(self.Pcbgolf_4_06, Transform((2.9968, 49.042)))
        self.place(self.Pcbgolf_4_07, Transform((2.9968, 51.069)))
        self.place(self.Pcbgolf_4_08, Transform((2.9968, 53.096)))
        self.place(self.Pcbgolf_4_09, Transform((2.9968, 55.123)))
        self.place(self.Pcbgolf_4_10, Transform((2.9968, 57.15)))
        self.place(self.Pcbgolf_4_11, Transform((2.9968, 59.177)))
        self.place(self.Pcbgolf_4_12, Transform((2.9968, 61.204)))
        self.place(self.Pcbgolf_4_13, Transform((2.9968, 63.231)))
        self.place(self.Pcbgolf_4_14, Transform((0, 34.853)))
        self.place(self.Pcbgolf_4_15, Transform((0, 36.88)))
        self.place(self.Pcbgolf_4_16, Transform((39.761, 7.1283)))
        self.place(self.Pcbgolf_4_17, Transform((22.3798, 0)))
        self.place(self.Pcbgolf_4_18, Transform((22.3798, 3.727)))
        self.place(self.Pcbgolf_4_19, Transform((22.3798, 7.454)))
        self.place(self.Pcbgolf_4_20, Transform((22.3798, 11.181)))
        self.place(self.Pcbgolf_4_21, Transform((11.9872, 31.481)))
        self.place(self.Pcbgolf_4_22, Transform((11.9872, 36.88)))
        self.place(self.Pcbgolf_4_23, Transform((11.9872, 38.907)))
        self.place(self.Pcbgolf_4_24, Transform((11.9872, 40.934)))
        self.place(self.Pcbgolf_4_25, Transform((11.9872, 42.961)))


from .components.UNKNOWN import QS5K2TR as QS5K2TR
from .components.UNKNOWN import RC0402FR_0710KL as RC0402FR_0710KL
from .components.UNKNOWN import RC0402JR_071KL as RC0402JR_071KL
from .components.UNKNOWN import RC0402JR_07100RL as RC0402JR_07100RL
class Pcbgolf_5_01(Circuit):
    CH3_SBU1_1 = Port()
    CH3_SBU1_IGN_1 = Port()
    CH3_SBU1_RELAY_1 = Port()
    GND_1 = Port()

    Q4 = QS5K2TR.Device()
    R100 = RC0402FR_0710KL.Device()
    R80 = RC0402FR_0710KL.Device()
    R94 = RC0402JR_071KL.Device()
    R95 = RC0402JR_07100RL.Device()

    nets = [
        Net([Q4.D1, R94.p[1]], name="Net_Q4_D1"),
        Net([Q4.D2, R95.p[1]], name="Net_Q4_D2"),
        Net([CH3_SBU1_1, R94.p[2], R95.p[2]], name="CH3_SBU1"),
        Net([CH3_SBU1_IGN_1, Q4.G1, R80.p[1]], name="CH3_SBU1_IGN"),
        Net([CH3_SBU1_RELAY_1, Q4.G2, R100.p[2]], name="CH3_SBU1_RELAY"),
        Net([GND_1, Q4.S, R100.p[1], R80.p[2]], name="GND"),
    ]

    def __init__(self):
        self.place(self.Q4, Transform((17.194, 0)))
        self.place(self.R100, Transform((5.9936, 23.6786)))
        self.place(self.R80, Transform((0, 3.4086)))
        self.place(self.R94, Transform((2.9968, 5.4356)))
        self.place(self.R95, Transform((2.9968, 3.4086)))



from .components.UNKNOWN import QS5K2TR as QS5K2TR
from .components.UNKNOWN import RC0402FR_0710KL as RC0402FR_0710KL
from .components.UNKNOWN import RC0402JR_071KL as RC0402JR_071KL
from .components.UNKNOWN import RC0402JR_07100RL as RC0402JR_07100RL
class Pcbgolf_5_02(Circuit):
    CH2_SBU1_1 = Port()
    CH2_SBU1_IGN_1 = Port()
    CH2_SBU1_RELAY_1 = Port()
    GND_1 = Port()

    Q3 = QS5K2TR.Device()
    R79 = RC0402FR_0710KL.Device()
    R92 = RC0402JR_071KL.Device()
    R93 = RC0402JR_07100RL.Device()
    R99 = RC0402FR_0710KL.Device()

    nets = [
        Net([Q3.D1, R92.p[1]], name="Net_Q3_D1"),
        Net([Q3.D2, R93.p[1]], name="Net_Q3_D2"),
        Net([CH2_SBU1_1, R92.p[2], R93.p[2]], name="CH2_SBU1"),
        Net([CH2_SBU1_IGN_1, Q3.G1, R79.p[1]], name="CH2_SBU1_IGN"),
        Net([CH2_SBU1_RELAY_1, Q3.G2, R99.p[2]], name="CH2_SBU1_RELAY"),
        Net([GND_1, Q3.S, R79.p[2], R99.p[1]], name="GND"),
    ]

    def __init__(self):
        self.place(self.Q3, Transform((13.146, 0)))
        self.place(self.R79, Transform((0, 5.4356)))
        self.place(self.R92, Transform((2.9968, 9.4896)))
        self.place(self.R93, Transform((2.9968, 7.4626)))
        self.place(self.R99, Transform((5.9936, 25.7056)))



from .components.UNKNOWN import CL21A106KAYNNNE_1 as CL21A106KAYNNNE
from .components.UNKNOWN import Comp_10132328_10011LF as Comp_10132328_10011LF
from .components.UNKNOWN import LG_R971_KN_1 as LG_R971_KN_1
from .components.UNKNOWN import RK73H1ETTP2802F as RK73H1ETTP2802F
from .components.UNKNOWN import RC0402JR_0733KL as RC0402JR_0733KL
from .components.UNKNOWN import RC0402JR_073K3L as RC0402JR_073K3L
from .components.UNKNOWN import TPS25944ARVCR as TPS25944ARVCR
from .symbols.SymbolU_12V_2 import SymbolU_12V
class Pcbgolf_5_03(Circuit):
    CAN0_H_1 = Port()
    CAN0_L_1 = Port()
    CAN1_H_1 = Port()
    CAN1_L_1 = Port()
    CAN2_H_1 = Port()
    CAN2_L_1 = Port()
    CAN3_H_1 = Port()
    CAN3_L_1 = Port()
    CH3_D_N_1 = Port()
    CH3_D_P_1 = Port()
    CH3_IMON_1 = Port()
    CH3_PWR_EN_1 = Port()
    CH3_SBU1_1 = Port()
    CH3_SBU2_1 = Port()
    GND_1 = Port()
    U_12V = Port()

    C52 = CL21A106KAYNNNE.Device()
    J7 = Comp_10132328_10011LF.Device()
    LED8 = LG_R971_KN_1.Device()
    R68 = RK73H1ETTP2802F.Device()
    R72 = RC0402JR_0733KL.Device()
    R76 = RC0402JR_073K3L.Device()
    U15 = TPS25944ARVCR.Device()

    nets = [
        Net([J7.VBUS[0], J7.VBUS[1], J7.VBUS[2], J7.VBUS[3], R76.p[1], U15.VOUT], name="Net_J7_VBUS_PadA4"),
        Net([LED8.A, R76.p[2]], name="Net_LED8_PadA"),
        Net([R68.p[2], U15.ILIM], name="Net_U15_ILIM"),
        Net([CAN0_H_1, J7.TX1p], name="CAN0_H"),
        Net([CAN0_L_1, J7.TX1n], name="CAN0_L"),
        Net([CAN1_H_1, J7.RX2p], name="CAN1_H"),
        Net([CAN1_L_1, J7.RX2n], name="CAN1_L"),
        Net([CAN2_H_1, J7.TX2p], name="CAN2_H"),
        Net([CAN2_L_1, J7.TX2n], name="CAN2_L"),
        Net([CAN3_H_1, J7.RX1p], name="CAN3_H"),
        Net([CAN3_L_1, J7.RX1n], name="CAN3_L"),
        Net([CH3_D_N_1, J7.D_A, J7.D_B], name="CH3_D_N"),
        Net([CH3_D_P_1, J7.DA, J7.DB], name="CH3_D_P"),
        Net([CH3_IMON_1, R72.p[2], U15.IMON], name="CH3_IMON"),
        Net([CH3_PWR_EN_1, U15.EN], name="CH3_PWR_EN"),
        Net([CH3_SBU1_1, J7.SBU1], name="CH3_SBU1"),
        Net([CH3_SBU2_1, J7.SBU2], name="CH3_SBU2"),
        Net([GND_1, C52.p[2], J7.GND[0], J7.GND[1], J7.GND[2], J7.GND[3], J7.SHIELDA, J7.SHIELDB, LED8.C, R68.p[1], R72.p[1], U15.GND, U15.OVP, U15.PGTH], name="GND"),
        Net([U_12V, C52.p[1], U15.VIN], name="Net12V", symbol=SymbolU_12V()),
    ]

    def __init__(self):
        self.place(self.C52, Transform((47.91505, 37.7395)))
        self.place(self.J7, Transform((32.77375, 41.45)))
        self.place(self.LED8, Transform((52.75305, 24.6865)))
        self.place(self.R68, Transform((9.01355, 52.3825)))
        self.place(self.R72, Transform((9.01355, 44.2745)))
        self.place(self.R76, Transform((9.01355, 36.1665)))
        self.place(self.U15, Transform((0, 0)))



from .components.UNKNOWN import QS5K2TR as QS5K2TR
from .components.UNKNOWN import RC0402FR_0710KL as RC0402FR_0710KL
from .components.UNKNOWN import RC0402JR_071KL as RC0402JR_071KL
from .components.UNKNOWN import RC0402JR_07100RL as RC0402JR_07100RL
class Pcbgolf_5_04(Circuit):
    CH3_SBU2_1 = Port()
    CH3_SBU2_IGN_1 = Port()
    CH3_SBU2_RELAY_1 = Port()
    GND_1 = Port()

    Q8 = QS5K2TR.Device()
    R104 = RC0402FR_0710KL.Device()
    R118 = RC0402JR_071KL.Device()
    R119 = RC0402JR_07100RL.Device()
    R124 = RC0402FR_0710KL.Device()

    nets = [
        Net([Q8.D1, R118.p[1]], name="Net_Q8_D1"),
        Net([Q8.D2, R119.p[1]], name="Net_Q8_D2"),
        Net([CH3_SBU2_1, R118.p[2], R119.p[2]], name="CH3_SBU2"),
        Net([CH3_SBU2_IGN_1, Q8.G1, R104.p[1]], name="CH3_SBU2_IGN"),
        Net([CH3_SBU2_RELAY_1, Q8.G2, R124.p[2]], name="CH3_SBU2_RELAY"),
        Net([GND_1, Q8.S, R104.p[2], R124.p[1]], name="GND"),
    ]

    def __init__(self):
        self.place(self.Q8, Transform((7.1524, 0)))
        self.place(self.R104, Transform((0, 20.3708)))
        self.place(self.R118, Transform((2.9968, 22.3978)))
        self.place(self.R119, Transform((2.9968, 20.3708)))
        self.place(self.R124, Transform((2.9968, 10.2358)))



from .components.UNKNOWN import CL21A106KAYNNNE_1 as CL21A106KAYNNNE
from .components.UNKNOWN import Comp_10132328_10011LF as Comp_10132328_10011LF
from .components.UNKNOWN import LG_R971_KN_1 as LG_R971_KN_1
from .components.UNKNOWN import RK73H1ETTP2802F as RK73H1ETTP2802F
from .components.UNKNOWN import RC0402JR_0733KL as RC0402JR_0733KL
from .components.UNKNOWN import RC0402JR_073K3L as RC0402JR_073K3L
from .components.UNKNOWN import TPS25944ARVCR as TPS25944ARVCR
from .symbols.SymbolU_12V_2 import SymbolU_12V
class Pcbgolf_5_05(Circuit):
    CAN0_H_1 = Port()
    CAN0_L_1 = Port()
    CAN1_H_1 = Port()
    CAN1_L_1 = Port()
    CAN2_H_1 = Port()
    CAN2_L_1 = Port()
    CAN3_H_1 = Port()
    CAN3_L_1 = Port()
    CH4_D_N_1 = Port()
    CH4_D_P_1 = Port()
    CH4_IMON_1 = Port()
    CH4_PWR_EN_1 = Port()
    CH4_SBU1_1 = Port()
    CH4_SBU2_1 = Port()
    GND_1 = Port()
    U_12V = Port()

    C53 = CL21A106KAYNNNE.Device()
    J8 = Comp_10132328_10011LF.Device()
    LED9 = LG_R971_KN_1.Device()
    R69 = RK73H1ETTP2802F.Device()
    R73 = RC0402JR_0733KL.Device()
    R77 = RC0402JR_073K3L.Device()
    U16 = TPS25944ARVCR.Device()

    nets = [
        Net([J8.VBUS[0], J8.VBUS[1], J8.VBUS[2], J8.VBUS[3], R77.p[1], U16.VOUT], name="Net_J8_VBUS_PadA4"),
        Net([LED9.A, R77.p[2]], name="Net_LED9_PadA"),
        Net([R69.p[2], U16.ILIM], name="Net_U16_ILIM"),
        Net([CAN0_H_1, J8.TX1p], name="CAN0_H"),
        Net([CAN0_L_1, J8.TX1n], name="CAN0_L"),
        Net([CAN1_H_1, J8.RX2p], name="CAN1_H"),
        Net([CAN1_L_1, J8.RX2n], name="CAN1_L"),
        Net([CAN2_H_1, J8.TX2p], name="CAN2_H"),
        Net([CAN2_L_1, J8.TX2n], name="CAN2_L"),
        Net([CAN3_H_1, J8.RX1p], name="CAN3_H"),
        Net([CAN3_L_1, J8.RX1n], name="CAN3_L"),
        Net([CH4_D_N_1, J8.D_A, J8.D_B], name="CH4_D_N"),
        Net([CH4_D_P_1, J8.DA, J8.DB], name="CH4_D_P"),
        Net([CH4_IMON_1, R73.p[2], U16.IMON], name="CH4_IMON"),
        Net([CH4_PWR_EN_1, U16.EN], name="CH4_PWR_EN"),
        Net([CH4_SBU1_1, J8.SBU1], name="CH4_SBU1"),
        Net([CH4_SBU2_1, J8.SBU2], name="CH4_SBU2"),
        Net([GND_1, C53.p[2], J8.GND[0], J8.GND[1], J8.GND[2], J8.GND[3], J8.SHIELDA, J8.SHIELDB, LED9.C, R69.p[1], R73.p[1], U16.GND, U16.OVP, U16.PGTH], name="GND"),
        Net([U_12V, C53.p[1], U16.VIN], name="Net12V", symbol=SymbolU_12V()),
    ]

    def __init__(self):
        self.place(self.C53, Transform((42.69423, 35.0125)))
        self.place(self.J8, Transform((27.55293, 35.05)))
        self.place(self.LED9, Transform((50.05923, 24.6865)))
        self.place(self.R69, Transform((3.79273, 50.3555)))
        self.place(self.R73, Transform((3.79273, 42.2475)))
        self.place(self.R77, Transform((3.79273, 34.1395)))
        self.place(self.U16, Transform((0, 0)))



from .components.UNKNOWN import QS5K2TR as QS5K2TR
from .components.UNKNOWN import RC0402FR_0710KL as RC0402FR_0710KL
from .components.UNKNOWN import RC0402JR_071KL as RC0402JR_071KL
from .components.UNKNOWN import RC0402JR_07100RL as RC0402JR_07100RL
class Pcbgolf_5_06(Circuit):
    CH1_SBU2_1 = Port()
    CH1_SBU2_IGN_1 = Port()
    CH1_SBU2_RELAY_1 = Port()
    GND_1 = Port()

    Q6 = QS5K2TR.Device()
    R102 = RC0402FR_0710KL.Device()
    R114 = RC0402JR_071KL.Device()
    R115 = RC0402JR_07100RL.Device()
    R122 = RC0402FR_0710KL.Device()

    nets = [
        Net([Q6.D1, R114.p[1]], name="Net_Q6_D1"),
        Net([Q6.D2, R115.p[1]], name="Net_Q6_D2"),
        Net([CH1_SBU2_1, R114.p[2], R115.p[2]], name="CH1_SBU2"),
        Net([CH1_SBU2_IGN_1, Q6.G1, R102.p[1]], name="CH1_SBU2_IGN"),
        Net([CH1_SBU2_RELAY_1, Q6.G2, R122.p[2]], name="CH1_SBU2_RELAY"),
        Net([GND_1, Q6.S, R102.p[2], R122.p[1]], name="GND"),
    ]

    def __init__(self):
        self.place(self.Q6, Transform((19.2964, 0)))
        self.place(self.R102, Transform((0, 19.6246)))
        self.place(self.R114, Transform((2.9968, 25.7056)))
        self.place(self.R115, Transform((2.9968, 23.6786)))
        self.place(self.R122, Transform((2.9968, 9.4896)))



from .components.UNKNOWN import CL21A106KAYNNNE_1 as CL21A106KAYNNNE
from .components.UNKNOWN import Comp_10132328_10011LF as Comp_10132328_10011LF
from .components.UNKNOWN import LG_R971_KN_1 as LG_R971_KN_1
from .components.UNKNOWN import RK73H1ETTP2802F as RK73H1ETTP2802F
from .components.UNKNOWN import RC0402JR_0733KL as RC0402JR_0733KL
from .components.UNKNOWN import RC0402JR_073K3L as RC0402JR_073K3L
from .components.UNKNOWN import TPS25944ARVCR as TPS25944ARVCR
from .symbols.SymbolU_12V_2 import SymbolU_12V
class Pcbgolf_5_07(Circuit):
    CAN0_H_1 = Port()
    CAN0_L_1 = Port()
    CAN1_H_1 = Port()
    CAN1_L_1 = Port()
    CAN2_H_1 = Port()
    CAN2_L_1 = Port()
    CAN3_H_1 = Port()
    CAN3_L_1 = Port()
    CH2_D_N_1 = Port()
    CH2_D_P_1 = Port()
    CH2_IMON_1 = Port()
    CH2_PWR_EN_1 = Port()
    CH2_SBU1_1 = Port()
    CH2_SBU2_1 = Port()
    GND_1 = Port()
    U_12V = Port()

    C51 = CL21A106KAYNNNE.Device()
    J6 = Comp_10132328_10011LF.Device()
    LED7 = LG_R971_KN_1.Device()
    R67 = RK73H1ETTP2802F.Device()
    R71 = RC0402JR_0733KL.Device()
    R75 = RC0402JR_073K3L.Device()
    U14 = TPS25944ARVCR.Device()

    nets = [
        Net([J6.VBUS[0], J6.VBUS[1], J6.VBUS[2], J6.VBUS[3], R75.p[1], U14.VOUT], name="Net_J6_VBUS_PadA4"),
        Net([LED7.A, R75.p[2]], name="Net_LED7_PadA"),
        Net([R67.p[2], U14.ILIM], name="Net_U14_ILIM"),
        Net([CAN0_H_1, J6.TX1p], name="CAN0_H"),
        Net([CAN0_L_1, J6.TX1n], name="CAN0_L"),
        Net([CAN1_H_1, J6.RX2p], name="CAN1_H"),
        Net([CAN1_L_1, J6.RX2n], name="CAN1_L"),
        Net([CAN2_H_1, J6.TX2p], name="CAN2_H"),
        Net([CAN2_L_1, J6.TX2n], name="CAN2_L"),
        Net([CAN3_H_1, J6.RX1p], name="CAN3_H"),
        Net([CAN3_L_1, J6.RX1n], name="CAN3_L"),
        Net([CH2_D_N_1, J6.D_A, J6.D_B], name="CH2_D_N"),
        Net([CH2_D_P_1, J6.DA, J6.DB], name="CH2_D_P"),
        Net([CH2_IMON_1, R71.p[2], U14.IMON], name="CH2_IMON"),
        Net([CH2_PWR_EN_1, U14.EN], name="CH2_PWR_EN"),
        Net([CH2_SBU1_1, J6.SBU1], name="CH2_SBU1"),
        Net([CH2_SBU2_1, J6.SBU2], name="CH2_SBU2"),
        Net([GND_1, C51.p[2], J6.GND[0], J6.GND[1], J6.GND[2], J6.GND[3], J6.SHIELDA, J6.SHIELDB, LED7.C, R67.p[1], R71.p[1], U14.GND, U14.OVP, U14.PGTH], name="GND"),
        Net([U_12V, C51.p[1], U14.VIN], name="Net12V", symbol=SymbolU_12V()),
    ]

    def __init__(self):
        self.place(self.C51, Transform((53.13586, 40.4665)))
        self.place(self.J6, Transform((37.99456, 47.85)))
        self.place(self.LED7, Transform((55.44686, 24.6865)))
        self.place(self.R67, Transform((14.23436, 54.4095)))
        self.place(self.R71, Transform((14.23436, 46.3015)))
        self.place(self.R75, Transform((14.23436, 38.1935)))
        self.place(self.U14, Transform((0, 0)))



from .components.UNKNOWN import CL21A106KAYNNNE_1 as CL21A106KAYNNNE
from .components.UNKNOWN import Comp_10132328_10011LF as Comp_10132328_10011LF
from .components.UNKNOWN import LG_R971_KN_1 as LG_R971_KN_1
from .components.UNKNOWN import RK73H1ETTP2802F as RK73H1ETTP2802F
from .components.UNKNOWN import RC0402JR_0733KL as RC0402JR_0733KL
from .components.UNKNOWN import RC0402JR_073K3L as RC0402JR_073K3L
from .components.UNKNOWN import TPS25944ARVCR as TPS25944ARVCR
from .symbols.SymbolU_12V_2 import SymbolU_12V
class Pcbgolf_5_08(Circuit):
    CAN0_H_1 = Port()
    CAN0_L_1 = Port()
    CAN1_H_1 = Port()
    CAN1_L_1 = Port()
    CAN2_H_1 = Port()
    CAN2_L_1 = Port()
    CAN3_H_1 = Port()
    CAN3_L_1 = Port()
    CH1_D_N_1 = Port()
    CH1_D_P_1 = Port()
    CH1_IMON_1 = Port()
    CH1_PWR_EN_1 = Port()
    CH1_SBU1_1 = Port()
    CH1_SBU2_1 = Port()
    GND_1 = Port()
    U_12V = Port()

    C50 = CL21A106KAYNNNE.Device()
    J5 = Comp_10132328_10011LF.Device()
    LED6 = LG_R971_KN_1.Device()
    R66 = RK73H1ETTP2802F.Device()
    R70 = RC0402JR_0733KL.Device()
    R74 = RC0402JR_073K3L.Device()
    U13 = TPS25944ARVCR.Device()

    nets = [
        Net([J5.VBUS[0], J5.VBUS[1], J5.VBUS[2], J5.VBUS[3], R74.p[1], U13.VOUT], name="Net_J5_VBUS_PadA4"),
        Net([LED6.A, R74.p[2]], name="Net_LED6_PadA"),
        Net([R66.p[2], U13.ILIM], name="Net_U13_ILIM"),
        Net([CAN0_H_1, J5.TX1p], name="CAN0_H"),
        Net([CAN0_L_1, J5.TX1n], name="CAN0_L"),
        Net([CAN1_H_1, J5.RX2p], name="CAN1_H"),
        Net([CAN1_L_1, J5.RX2n], name="CAN1_L"),
        Net([CAN2_H_1, J5.TX2p], name="CAN2_H"),
        Net([CAN2_L_1, J5.TX2n], name="CAN2_L"),
        Net([CAN3_H_1, J5.RX1p], name="CAN3_H"),
        Net([CAN3_L_1, J5.RX1n], name="CAN3_L"),
        Net([CH1_D_N_1, J5.D_A, J5.D_B], name="CH1_D_N"),
        Net([CH1_D_P_1, J5.DA, J5.DB], name="CH1_D_P"),
        Net([CH1_IMON_1, R70.p[2], U13.IMON], name="CH1_IMON"),
        Net([CH1_PWR_EN_1, U13.EN], name="CH1_PWR_EN"),
        Net([CH1_SBU1_1, J5.SBU1], name="CH1_SBU1"),
        Net([CH1_SBU2_1, J5.SBU2], name="CH1_SBU2"),
        Net([GND_1, C50.p[2], J5.GND[0], J5.GND[1], J5.GND[2], J5.GND[3], J5.SHIELDA, J5.SHIELDB, LED6.C, R66.p[1], R70.p[1], U13.GND, U13.OVP, U13.PGTH], name="GND"),
        Net([U_12V, C50.p[1], U13.VIN], name="Net12V", symbol=SymbolU_12V()),
    ]

    def __init__(self):
        self.place(self.C50, Transform((54.22968, 29.5585)))
        self.place(self.J5, Transform((43.21538, 54.25)))
        self.place(self.LED6, Transform((58.14068, 24.6865)))
        self.place(self.R66, Transform((19.45518, 56.4365)))
        self.place(self.R70, Transform((19.45518, 48.3285)))
        self.place(self.R74, Transform((19.45518, 40.2205)))
        self.place(self.U13, Transform((0, 0)))



from .components.UNKNOWN import AM23ESGW as AM23ESGW
from .components.UNKNOWN import RC0402JR_07100RL as RC0402JR_07100RL
class Pcbgolf_5_09(Circuit):
    CH2_SBU1_IGN_1 = Port()
    CH2_SBU1_RELAY_1 = Port()
    GND_1 = Port()

    LED11 = AM23ESGW.Device()
    R84 = RC0402JR_07100RL.Device()
    R85 = RC0402JR_07100RL.Device()

    nets = [
        Net([LED11.AG, R84.p[1]], name="Net_LED11_AG"),
        Net([LED11.AR, R85.p[1]], name="Net_LED11_AR"),
        Net([CH2_SBU1_IGN_1, R85.p[2]], name="CH2_SBU1_IGN"),
        Net([CH2_SBU1_RELAY_1, R84.p[2]], name="CH2_SBU1_RELAY"),
        Net([GND_1, LED11.C], name="GND"),
    ]

    def __init__(self):
        self.place(self.LED11, Transform((6.3407, 0)))
        self.place(self.R84, Transform((0, 38.9555)))
        self.place(self.R85, Transform((0, 36.9285)))



from .components.UNKNOWN import QS5K2TR as QS5K2TR
from .components.UNKNOWN import RC0402FR_0710KL as RC0402FR_0710KL
from .components.UNKNOWN import RC0402JR_071KL as RC0402JR_071KL
from .components.UNKNOWN import RC0402JR_07100RL as RC0402JR_07100RL
class Pcbgolf_5_10(Circuit):
    CH2_SBU2_1 = Port()
    CH2_SBU2_IGN_1 = Port()
    CH2_SBU2_RELAY_1 = Port()
    GND_1 = Port()

    Q7 = QS5K2TR.Device()
    R103 = RC0402FR_0710KL.Device()
    R116 = RC0402JR_071KL.Device()
    R117 = RC0402JR_07100RL.Device()
    R123 = RC0402FR_0710KL.Device()

    nets = [
        Net([Q7.D1, R116.p[1]], name="Net_Q7_D1"),
        Net([Q7.D2, R117.p[1]], name="Net_Q7_D2"),
        Net([CH2_SBU2_1, R116.p[2], R117.p[2]], name="CH2_SBU2"),
        Net([CH2_SBU2_IGN_1, Q7.G1, R103.p[1]], name="CH2_SBU2_IGN"),
        Net([CH2_SBU2_RELAY_1, Q7.G2, R123.p[2]], name="CH2_SBU2_RELAY"),
        Net([GND_1, Q7.S, R103.p[2], R123.p[1]], name="GND"),
    ]

    def __init__(self):
        self.place(self.Q7, Transform((3.1044, 0)))
        self.place(self.R103, Transform((0, 22.3978)))
        self.place(self.R116, Transform((2.9968, 26.4518)))
        self.place(self.R117, Transform((2.9968, 24.4248)))
        self.place(self.R123, Transform((2.9968, 12.2628)))



from .components.UNKNOWN import QS5K2TR as QS5K2TR
from .components.UNKNOWN import RC0402FR_0710KL as RC0402FR_0710KL
from .components.UNKNOWN import RC0402JR_071KL as RC0402JR_071KL
from .components.UNKNOWN import RC0402JR_07100RL as RC0402JR_07100RL
class Pcbgolf_5_11(Circuit):
    CH4_SBU1_1 = Port()
    CH4_SBU1_IGN_1 = Port()
    CH4_SBU1_RELAY_1 = Port()
    GND_1 = Port()

    Q5 = QS5K2TR.Device()
    R101 = RC0402FR_0710KL.Device()
    R81 = RC0402FR_0710KL.Device()
    R96 = RC0402JR_071KL.Device()
    R97 = RC0402JR_07100RL.Device()

    nets = [
        Net([Q5.D1, R96.p[1]], name="Net_Q5_D1"),
        Net([Q5.D2, R97.p[1]], name="Net_Q5_D2"),
        Net([CH4_SBU1_1, R96.p[2], R97.p[2]], name="CH4_SBU1"),
        Net([CH4_SBU1_IGN_1, Q5.G1, R81.p[1]], name="CH4_SBU1_IGN"),
        Net([CH4_SBU1_RELAY_1, Q5.G2, R101.p[2]], name="CH4_SBU1_RELAY"),
        Net([GND_1, Q5.S, R101.p[1], R81.p[2]], name="GND"),
    ]

    def __init__(self):
        self.place(self.Q5, Transform((18.2452, 0)))
        self.place(self.R101, Transform((2.9968, 21.6516)))
        self.place(self.R81, Transform((0, 31.7866)))
        self.place(self.R96, Transform((2.9968, 31.7866)))
        self.place(self.R97, Transform((2.9968, 29.7596)))



from .components.UNKNOWN import QS5K2TR as QS5K2TR
from .components.UNKNOWN import RC0402FR_0710KL as RC0402FR_0710KL
from .components.UNKNOWN import RC0402JR_071KL as RC0402JR_071KL
from .components.UNKNOWN import RC0402JR_07100RL as RC0402JR_07100RL
class Pcbgolf_5_12(Circuit):
    CH1_SBU1_1 = Port()
    CH1_SBU1_IGN_1 = Port()
    CH1_SBU1_RELAY_1 = Port()
    GND_1 = Port()

    Q2 = QS5K2TR.Device()
    R78 = RC0402FR_0710KL.Device()
    R90 = RC0402JR_071KL.Device()
    R91 = RC0402JR_07100RL.Device()
    R98 = RC0402FR_0710KL.Device()

    nets = [
        Net([Q2.D1, R90.p[1]], name="Net_Q2_D1"),
        Net([Q2.D2, R91.p[1]], name="Net_Q2_D2"),
        Net([CH1_SBU1_1, R90.p[2], R91.p[2]], name="CH1_SBU1"),
        Net([CH1_SBU1_IGN_1, Q2.G1, R78.p[1]], name="CH1_SBU1_IGN"),
        Net([CH1_SBU1_RELAY_1, Q2.G2, R98.p[2]], name="CH1_SBU1_RELAY"),
        Net([GND_1, Q2.S, R78.p[2], R98.p[1]], name="GND"),
    ]

    def __init__(self):
        self.place(self.Q2, Transform((9.098, 0)))
        self.place(self.R78, Transform((0, 7.4626)))
        self.place(self.R90, Transform((2.9968, 13.5436)))
        self.place(self.R91, Transform((2.9968, 11.5166)))
        self.place(self.R98, Transform((5.9936, 27.7326)))



from .components.UNKNOWN import AM23ESGW as AM23ESGW
from .components.UNKNOWN import RC0402JR_07100RL as RC0402JR_07100RL
class Pcbgolf_5_13(Circuit):
    CH4_SBU2_IGN_1 = Port()
    CH4_SBU2_RELAY_1 = Port()
    GND_1 = Port()

    LED17 = AM23ESGW.Device()
    R112 = RC0402JR_07100RL.Device()
    R113 = RC0402JR_07100RL.Device()

    nets = [
        Net([LED17.AG, R112.p[1]], name="Net_LED17_AG"),
        Net([LED17.AR, R113.p[1]], name="Net_LED17_AR"),
        Net([CH4_SBU2_IGN_1, R113.p[2]], name="CH4_SBU2_IGN"),
        Net([CH4_SBU2_RELAY_1, R112.p[2]], name="CH4_SBU2_RELAY"),
        Net([GND_1, LED17.C], name="GND"),
    ]

    def __init__(self):
        self.place(self.LED17, Transform((4.8741, 0)))
        self.place(self.R112, Transform((0, 47.0095)))
        self.place(self.R113, Transform((0, 44.9825)))



from .components.UNKNOWN import AM23ESGW as AM23ESGW
from .components.UNKNOWN import RC0402JR_07100RL as RC0402JR_07100RL
class Pcbgolf_5_14(Circuit):
    CH3_SBU2_IGN_1 = Port()
    CH3_SBU2_RELAY_1 = Port()
    GND_1 = Port()

    LED16 = AM23ESGW.Device()
    R110 = RC0402JR_07100RL.Device()
    R111 = RC0402JR_07100RL.Device()

    nets = [
        Net([LED16.AG, R110.p[1]], name="Net_LED16_AG"),
        Net([LED16.AR, R111.p[1]], name="Net_LED16_AR"),
        Net([CH3_SBU2_IGN_1, R111.p[2]], name="CH3_SBU2_IGN"),
        Net([CH3_SBU2_RELAY_1, R110.p[2]], name="CH3_SBU2_RELAY"),
        Net([GND_1, LED16.C], name="GND"),
    ]

    def __init__(self):
        self.place(self.LED16, Transform((7.8709, 0)))
        self.place(self.R110, Transform((0, 16.6585)))
        self.place(self.R111, Transform((2.9968, 45.0365)))



from .components.UNKNOWN import AM23ESGW as AM23ESGW
from .components.UNKNOWN import RC0402JR_07100RL as RC0402JR_07100RL
class Pcbgolf_5_15(Circuit):
    CH2_SBU2_IGN_1 = Port()
    CH2_SBU2_RELAY_1 = Port()
    GND_1 = Port()

    LED15 = AM23ESGW.Device()
    R108 = RC0402JR_07100RL.Device()
    R109 = RC0402JR_07100RL.Device()

    nets = [
        Net([LED15.AG, R108.p[1]], name="Net_LED15_AG"),
        Net([LED15.AR, R109.p[1]], name="Net_LED15_AR"),
        Net([CH2_SBU2_IGN_1, R109.p[2]], name="CH2_SBU2_IGN"),
        Net([CH2_SBU2_RELAY_1, R108.p[2]], name="CH2_SBU2_RELAY"),
        Net([GND_1, LED15.C], name="GND"),
    ]

    def __init__(self):
        self.place(self.LED15, Transform((7.8709, 0)))
        self.place(self.R108, Transform((0, 16.7125)))
        self.place(self.R109, Transform((0, 14.6855)))



from .components.UNKNOWN import AM23ESGW as AM23ESGW
from .components.UNKNOWN import RC0402JR_07100RL as RC0402JR_07100RL
class Pcbgolf_5_16(Circuit):
    CH1_SBU2_IGN_1 = Port()
    CH1_SBU2_RELAY_1 = Port()
    GND_1 = Port()

    LED14 = AM23ESGW.Device()
    R106 = RC0402JR_07100RL.Device()
    R107 = RC0402JR_07100RL.Device()

    nets = [
        Net([LED14.AG, R106.p[1]], name="Net_LED14_AG"),
        Net([LED14.AR, R107.p[1]], name="Net_LED14_AR"),
        Net([CH1_SBU2_IGN_1, R107.p[2]], name="CH1_SBU2_IGN"),
        Net([CH1_SBU2_RELAY_1, R106.p[2]], name="CH1_SBU2_RELAY"),
        Net([GND_1, LED14.C], name="GND"),
    ]

    def __init__(self):
        self.place(self.LED14, Transform((3.3439, 0)))
        self.place(self.R106, Transform((0, 36.7665)))
        self.place(self.R107, Transform((0, 34.7395)))



from .components.UNKNOWN import AM23ESGW as AM23ESGW
from .components.UNKNOWN import RC0402JR_07100RL as RC0402JR_07100RL
class Pcbgolf_5_17(Circuit):
    CH4_SBU1_IGN_1 = Port()
    CH4_SBU1_RELAY_1 = Port()
    GND_1 = Port()

    LED13 = AM23ESGW.Device()
    R88 = RC0402JR_07100RL.Device()
    R89 = RC0402JR_07100RL.Device()

    nets = [
        Net([LED13.AG, R88.p[1]], name="Net_LED13_AG"),
        Net([LED13.AR, R89.p[1]], name="Net_LED13_AR"),
        Net([CH4_SBU1_IGN_1, R89.p[2]], name="CH4_SBU1_IGN"),
        Net([CH4_SBU1_RELAY_1, R88.p[2]], name="CH4_SBU1_RELAY"),
        Net([GND_1, LED13.C], name="GND"),
    ]

    def __init__(self):
        self.place(self.LED13, Transform((6.3407, 0)))
        self.place(self.R88, Transform((0, 38.8475)))
        self.place(self.R89, Transform((0, 36.8205)))



from .components.UNKNOWN import AM23ESGW as AM23ESGW
from .components.UNKNOWN import RC0402JR_07100RL as RC0402JR_07100RL
class Pcbgolf_5_18(Circuit):
    CH3_SBU1_IGN_1 = Port()
    CH3_SBU1_RELAY_1 = Port()
    GND_1 = Port()

    LED12 = AM23ESGW.Device()
    R86 = RC0402JR_07100RL.Device()
    R87 = RC0402JR_07100RL.Device()

    nets = [
        Net([LED12.AG, R86.p[1]], name="Net_LED12_AG"),
        Net([LED12.AR, R87.p[1]], name="Net_LED12_AR"),
        Net([CH3_SBU1_IGN_1, R87.p[2]], name="CH3_SBU1_IGN"),
        Net([CH3_SBU1_RELAY_1, R86.p[2]], name="CH3_SBU1_RELAY"),
        Net([GND_1, LED12.C], name="GND"),
    ]

    def __init__(self):
        self.place(self.LED12, Transform((6.3407, 0)))
        self.place(self.R86, Transform((0, 38.9015)))
        self.place(self.R87, Transform((0, 36.8745)))



from .components.UNKNOWN import AM23ESGW as AM23ESGW
from .components.UNKNOWN import RC0402JR_07100RL as RC0402JR_07100RL
class Pcbgolf_5_19(Circuit):
    CH1_SBU1_IGN_1 = Port()
    CH1_SBU1_RELAY_1 = Port()
    GND_1 = Port()

    LED10 = AM23ESGW.Device()
    R82 = RC0402JR_07100RL.Device()
    R83 = RC0402JR_07100RL.Device()

    nets = [
        Net([LED10.AG, R82.p[1]], name="Net_LED10_AG"),
        Net([LED10.AR, R83.p[1]], name="Net_LED10_AR"),
        Net([CH1_SBU1_IGN_1, R83.p[2]], name="CH1_SBU1_IGN"),
        Net([CH1_SBU1_RELAY_1, R82.p[2]], name="CH1_SBU1_RELAY"),
        Net([GND_1, LED10.C], name="GND"),
    ]

    def __init__(self):
        self.place(self.LED10, Transform((6.3407, 0)))
        self.place(self.R82, Transform((0, 39.0095)))
        self.place(self.R83, Transform((0, 36.9825)))



from .components.UNKNOWN import QS5K2TR as QS5K2TR
from .components.UNKNOWN import RC0402FR_0710KL as RC0402FR_0710KL
from .components.UNKNOWN import RC0402JR_071KL as RC0402JR_071KL
from .components.UNKNOWN import RC0402JR_07100RL as RC0402JR_07100RL
class Pcbgolf_5_20(Circuit):
    CH4_SBU2_1 = Port()
    CH4_SBU2_IGN_1 = Port()
    CH4_SBU2_RELAY_1 = Port()
    GND_1 = Port()

    Q9 = QS5K2TR.Device()
    R105 = RC0402FR_0710KL.Device()
    R120 = RC0402JR_071KL.Device()
    R121 = RC0402JR_07100RL.Device()
    R125 = RC0402FR_0710KL.Device()

    nets = [
        Net([Q9.D1, R120.p[1]], name="Net_Q9_D1"),
        Net([Q9.D2, R121.p[1]], name="Net_Q9_D2"),
        Net([CH4_SBU2_1, R120.p[2], R121.p[2]], name="CH4_SBU2"),
        Net([CH4_SBU2_IGN_1, Q9.G1, R105.p[1]], name="CH4_SBU2_IGN"),
        Net([CH4_SBU2_RELAY_1, Q9.G2, R125.p[2]], name="CH4_SBU2_RELAY"),
        Net([GND_1, Q9.S, R105.p[2], R125.p[1]], name="GND"),
    ]

    def __init__(self):
        self.place(self.Q9, Transform((11.2004, 0)))
        self.place(self.R105, Transform((0, 18.3438)))
        self.place(self.R120, Transform((2.9968, 18.3438)))
        self.place(self.R121, Transform((2.9968, 16.3168)))
        self.place(self.R125, Transform((2.9968, 8.2088)))



from .symbols.SymbolU_12V_2 import SymbolU_12V
class Pcbgolf_5(Circuit):
    CAN0_H_1 = Port()
    CAN0_L_1 = Port()
    CAN1_H_1 = Port()
    CAN1_L_1 = Port()
    CAN2_H_1 = Port()
    CAN2_L_1 = Port()
    CAN3_H_1 = Port()
    CAN3_L_1 = Port()
    CH1_D_N_1 = Port()
    CH1_D_P_1 = Port()
    CH1_IMON_1 = Port()
    CH1_PWR_EN_1 = Port()
    CH1_SBU1_1 = Port()
    CH1_SBU1_IGN_1 = Port()
    CH1_SBU1_RELAY_1 = Port()
    CH1_SBU2_1 = Port()
    CH1_SBU2_IGN_1 = Port()
    CH1_SBU2_RELAY_1 = Port()
    CH2_D_N_1 = Port()
    CH2_D_P_1 = Port()
    CH2_IMON_1 = Port()
    CH2_PWR_EN_1 = Port()
    CH2_SBU1_1 = Port()
    CH2_SBU1_IGN_1 = Port()
    CH2_SBU1_RELAY_1 = Port()
    CH2_SBU2_1 = Port()
    CH2_SBU2_IGN_1 = Port()
    CH2_SBU2_RELAY_1 = Port()
    CH3_D_N_1 = Port()
    CH3_D_P_1 = Port()
    CH3_IMON_1 = Port()
    CH3_PWR_EN_1 = Port()
    CH3_SBU1_1 = Port()
    CH3_SBU1_IGN_1 = Port()
    CH3_SBU1_RELAY_1 = Port()
    CH3_SBU2_1 = Port()
    CH3_SBU2_IGN_1 = Port()
    CH3_SBU2_RELAY_1 = Port()
    CH4_D_N_1 = Port()
    CH4_D_P_1 = Port()
    CH4_IMON_1 = Port()
    CH4_PWR_EN_1 = Port()
    CH4_SBU1_1 = Port()
    CH4_SBU1_IGN_1 = Port()
    CH4_SBU1_RELAY_1 = Port()
    CH4_SBU2_1 = Port()
    CH4_SBU2_IGN_1 = Port()
    CH4_SBU2_RELAY_1 = Port()
    GND_1 = Port()
    U_12V = Port()

    Pcbgolf_5_01 = Pcbgolf_5_01()
    Pcbgolf_5_02 = Pcbgolf_5_02()
    Pcbgolf_5_03 = Pcbgolf_5_03()
    Pcbgolf_5_04 = Pcbgolf_5_04()
    Pcbgolf_5_05 = Pcbgolf_5_05()
    Pcbgolf_5_06 = Pcbgolf_5_06()
    Pcbgolf_5_07 = Pcbgolf_5_07()
    Pcbgolf_5_08 = Pcbgolf_5_08()
    Pcbgolf_5_09 = Pcbgolf_5_09()
    Pcbgolf_5_10 = Pcbgolf_5_10()
    Pcbgolf_5_11 = Pcbgolf_5_11()
    Pcbgolf_5_12 = Pcbgolf_5_12()
    Pcbgolf_5_13 = Pcbgolf_5_13()
    Pcbgolf_5_14 = Pcbgolf_5_14()
    Pcbgolf_5_15 = Pcbgolf_5_15()
    Pcbgolf_5_16 = Pcbgolf_5_16()
    Pcbgolf_5_17 = Pcbgolf_5_17()
    Pcbgolf_5_18 = Pcbgolf_5_18()
    Pcbgolf_5_19 = Pcbgolf_5_19()
    Pcbgolf_5_20 = Pcbgolf_5_20()

    nets = [
        Net([CAN0_H_1, Pcbgolf_5_03.CAN0_H_1, Pcbgolf_5_05.CAN0_H_1, Pcbgolf_5_07.CAN0_H_1, Pcbgolf_5_08.CAN0_H_1], name="CAN0_H"),
        Net([CAN0_L_1, Pcbgolf_5_03.CAN0_L_1, Pcbgolf_5_05.CAN0_L_1, Pcbgolf_5_07.CAN0_L_1, Pcbgolf_5_08.CAN0_L_1], name="CAN0_L"),
        Net([CAN1_H_1, Pcbgolf_5_03.CAN1_H_1, Pcbgolf_5_05.CAN1_H_1, Pcbgolf_5_07.CAN1_H_1, Pcbgolf_5_08.CAN1_H_1], name="CAN1_H"),
        Net([CAN1_L_1, Pcbgolf_5_03.CAN1_L_1, Pcbgolf_5_05.CAN1_L_1, Pcbgolf_5_07.CAN1_L_1, Pcbgolf_5_08.CAN1_L_1], name="CAN1_L"),
        Net([CAN2_H_1, Pcbgolf_5_03.CAN2_H_1, Pcbgolf_5_05.CAN2_H_1, Pcbgolf_5_07.CAN2_H_1, Pcbgolf_5_08.CAN2_H_1], name="CAN2_H"),
        Net([CAN2_L_1, Pcbgolf_5_03.CAN2_L_1, Pcbgolf_5_05.CAN2_L_1, Pcbgolf_5_07.CAN2_L_1, Pcbgolf_5_08.CAN2_L_1], name="CAN2_L"),
        Net([CAN3_H_1, Pcbgolf_5_03.CAN3_H_1, Pcbgolf_5_05.CAN3_H_1, Pcbgolf_5_07.CAN3_H_1, Pcbgolf_5_08.CAN3_H_1], name="CAN3_H"),
        Net([CAN3_L_1, Pcbgolf_5_03.CAN3_L_1, Pcbgolf_5_05.CAN3_L_1, Pcbgolf_5_07.CAN3_L_1, Pcbgolf_5_08.CAN3_L_1], name="CAN3_L"),
        Net([CH1_D_N_1, Pcbgolf_5_08.CH1_D_N_1], name="CH1_D_N"),
        Net([CH1_D_P_1, Pcbgolf_5_08.CH1_D_P_1], name="CH1_D_P"),
        Net([CH1_IMON_1, Pcbgolf_5_08.CH1_IMON_1], name="CH1_IMON"),
        Net([CH1_PWR_EN_1, Pcbgolf_5_08.CH1_PWR_EN_1], name="CH1_PWR_EN"),
        Net([CH1_SBU1_1, Pcbgolf_5_08.CH1_SBU1_1, Pcbgolf_5_12.CH1_SBU1_1], name="CH1_SBU1"),
        Net([CH1_SBU1_IGN_1, Pcbgolf_5_12.CH1_SBU1_IGN_1, Pcbgolf_5_19.CH1_SBU1_IGN_1], name="CH1_SBU1_IGN"),
        Net([CH1_SBU1_RELAY_1, Pcbgolf_5_12.CH1_SBU1_RELAY_1, Pcbgolf_5_19.CH1_SBU1_RELAY_1], name="CH1_SBU1_RELAY"),
        Net([CH1_SBU2_1, Pcbgolf_5_06.CH1_SBU2_1, Pcbgolf_5_08.CH1_SBU2_1], name="CH1_SBU2"),
        Net([CH1_SBU2_IGN_1, Pcbgolf_5_06.CH1_SBU2_IGN_1, Pcbgolf_5_16.CH1_SBU2_IGN_1], name="CH1_SBU2_IGN"),
        Net([CH1_SBU2_RELAY_1, Pcbgolf_5_06.CH1_SBU2_RELAY_1, Pcbgolf_5_16.CH1_SBU2_RELAY_1], name="CH1_SBU2_RELAY"),
        Net([CH2_D_N_1, Pcbgolf_5_07.CH2_D_N_1], name="CH2_D_N"),
        Net([CH2_D_P_1, Pcbgolf_5_07.CH2_D_P_1], name="CH2_D_P"),
        Net([CH2_IMON_1, Pcbgolf_5_07.CH2_IMON_1], name="CH2_IMON"),
        Net([CH2_PWR_EN_1, Pcbgolf_5_07.CH2_PWR_EN_1], name="CH2_PWR_EN"),
        Net([CH2_SBU1_1, Pcbgolf_5_02.CH2_SBU1_1, Pcbgolf_5_07.CH2_SBU1_1], name="CH2_SBU1"),
        Net([CH2_SBU1_IGN_1, Pcbgolf_5_02.CH2_SBU1_IGN_1, Pcbgolf_5_09.CH2_SBU1_IGN_1], name="CH2_SBU1_IGN"),
        Net([CH2_SBU1_RELAY_1, Pcbgolf_5_02.CH2_SBU1_RELAY_1, Pcbgolf_5_09.CH2_SBU1_RELAY_1], name="CH2_SBU1_RELAY"),
        Net([CH2_SBU2_1, Pcbgolf_5_07.CH2_SBU2_1, Pcbgolf_5_10.CH2_SBU2_1], name="CH2_SBU2"),
        Net([CH2_SBU2_IGN_1, Pcbgolf_5_10.CH2_SBU2_IGN_1, Pcbgolf_5_15.CH2_SBU2_IGN_1], name="CH2_SBU2_IGN"),
        Net([CH2_SBU2_RELAY_1, Pcbgolf_5_10.CH2_SBU2_RELAY_1, Pcbgolf_5_15.CH2_SBU2_RELAY_1], name="CH2_SBU2_RELAY"),
        Net([CH3_D_N_1, Pcbgolf_5_03.CH3_D_N_1], name="CH3_D_N"),
        Net([CH3_D_P_1, Pcbgolf_5_03.CH3_D_P_1], name="CH3_D_P"),
        Net([CH3_IMON_1, Pcbgolf_5_03.CH3_IMON_1], name="CH3_IMON"),
        Net([CH3_PWR_EN_1, Pcbgolf_5_03.CH3_PWR_EN_1], name="CH3_PWR_EN"),
        Net([CH3_SBU1_1, Pcbgolf_5_01.CH3_SBU1_1, Pcbgolf_5_03.CH3_SBU1_1], name="CH3_SBU1"),
        Net([CH3_SBU1_IGN_1, Pcbgolf_5_01.CH3_SBU1_IGN_1, Pcbgolf_5_18.CH3_SBU1_IGN_1], name="CH3_SBU1_IGN"),
        Net([CH3_SBU1_RELAY_1, Pcbgolf_5_01.CH3_SBU1_RELAY_1, Pcbgolf_5_18.CH3_SBU1_RELAY_1], name="CH3_SBU1_RELAY"),
        Net([CH3_SBU2_1, Pcbgolf_5_03.CH3_SBU2_1, Pcbgolf_5_04.CH3_SBU2_1], name="CH3_SBU2"),
        Net([CH3_SBU2_IGN_1, Pcbgolf_5_04.CH3_SBU2_IGN_1, Pcbgolf_5_14.CH3_SBU2_IGN_1], name="CH3_SBU2_IGN"),
        Net([CH3_SBU2_RELAY_1, Pcbgolf_5_04.CH3_SBU2_RELAY_1, Pcbgolf_5_14.CH3_SBU2_RELAY_1], name="CH3_SBU2_RELAY"),
        Net([CH4_D_N_1, Pcbgolf_5_05.CH4_D_N_1], name="CH4_D_N"),
        Net([CH4_D_P_1, Pcbgolf_5_05.CH4_D_P_1], name="CH4_D_P"),
        Net([CH4_IMON_1, Pcbgolf_5_05.CH4_IMON_1], name="CH4_IMON"),
        Net([CH4_PWR_EN_1, Pcbgolf_5_05.CH4_PWR_EN_1], name="CH4_PWR_EN"),
        Net([CH4_SBU1_1, Pcbgolf_5_05.CH4_SBU1_1, Pcbgolf_5_11.CH4_SBU1_1], name="CH4_SBU1"),
        Net([CH4_SBU1_IGN_1, Pcbgolf_5_11.CH4_SBU1_IGN_1, Pcbgolf_5_17.CH4_SBU1_IGN_1], name="CH4_SBU1_IGN"),
        Net([CH4_SBU1_RELAY_1, Pcbgolf_5_11.CH4_SBU1_RELAY_1, Pcbgolf_5_17.CH4_SBU1_RELAY_1], name="CH4_SBU1_RELAY"),
        Net([CH4_SBU2_1, Pcbgolf_5_05.CH4_SBU2_1, Pcbgolf_5_20.CH4_SBU2_1], name="CH4_SBU2"),
        Net([CH4_SBU2_IGN_1, Pcbgolf_5_13.CH4_SBU2_IGN_1, Pcbgolf_5_20.CH4_SBU2_IGN_1], name="CH4_SBU2_IGN"),
        Net([CH4_SBU2_RELAY_1, Pcbgolf_5_13.CH4_SBU2_RELAY_1, Pcbgolf_5_20.CH4_SBU2_RELAY_1], name="CH4_SBU2_RELAY"),
        Net([GND_1, Pcbgolf_5_01.GND_1, Pcbgolf_5_02.GND_1, Pcbgolf_5_03.GND_1, Pcbgolf_5_04.GND_1, Pcbgolf_5_05.GND_1, Pcbgolf_5_06.GND_1, Pcbgolf_5_07.GND_1, Pcbgolf_5_08.GND_1, Pcbgolf_5_09.GND_1, Pcbgolf_5_10.GND_1, Pcbgolf_5_11.GND_1, Pcbgolf_5_12.GND_1, Pcbgolf_5_13.GND_1, Pcbgolf_5_14.GND_1, Pcbgolf_5_15.GND_1, Pcbgolf_5_16.GND_1, Pcbgolf_5_17.GND_1, Pcbgolf_5_18.GND_1, Pcbgolf_5_19.GND_1, Pcbgolf_5_20.GND_1], name="GND"),
        Net([U_12V, Pcbgolf_5_03.U_12V, Pcbgolf_5_05.U_12V, Pcbgolf_5_07.U_12V, Pcbgolf_5_08.U_12V], name="Net12V", symbol=SymbolU_12V()),
    ]

    def __init__(self):
        self.place(self.Pcbgolf_5_01, Transform((19.45518, 25.2499)))
        self.place(self.Pcbgolf_5_02, Transform((19.45518, 25.2499)))
        self.place(self.Pcbgolf_5_03, Transform((10.44164, 0.6)))
        self.place(self.Pcbgolf_5_04, Transform((25.44878, 20.4497)))
        self.place(self.Pcbgolf_5_05, Transform((15.66245, 0.6)))
        self.place(self.Pcbgolf_5_06, Transform((25.44878, 25.2499)))
        self.place(self.Pcbgolf_5_07, Transform((5.22082, 0.6)))
        self.place(self.Pcbgolf_5_08, Transform((0, 0.6)))
        self.place(self.Pcbgolf_5_09, Transform((22.45198, 12)))
        self.place(self.Pcbgolf_5_10, Transform((25.44878, 20.4497)))
        self.place(self.Pcbgolf_5_11, Transform((22.45198, 25.2499)))
        self.place(self.Pcbgolf_5_12, Transform((19.45518, 25.2499)))
        self.place(self.Pcbgolf_5_13, Transform((28.44558, 8)))
        self.place(self.Pcbgolf_5_14, Transform((25.44878, 12)))
        self.place(self.Pcbgolf_5_15, Transform((25.44878, 16)))
        self.place(self.Pcbgolf_5_16, Transform((25.44878, 0)))
        self.place(self.Pcbgolf_5_17, Transform((22.45198, 4)))
        self.place(self.Pcbgolf_5_18, Transform((22.45198, 8)))
        self.place(self.Pcbgolf_5_19, Transform((22.45198, 16)))
        self.place(self.Pcbgolf_5_20, Transform((25.44878, 20.4497)))


from .components.UNKNOWN import CL21A106KAYNNNE as CL21A106KAYNNNE
from .components.UNKNOWN import CL05F104ZO5NNNC as CL05F104ZO5NNNC
from .components.UNKNOWN import comma_ai_11112255_C0402 as comma_ai_11112255_C0402
from .components.UNKNOWN import MEKK2520T3R3M as MEKK2520T3R3M
from .components.UNKNOWN import RC0402FR_0710KL as RC0402FR_0710KL
from .components.UNKNOWN import RC0402JR_07100KL as RC0402JR_07100KL
from .components.UNKNOWN import AP62300WU_7 as AP62300WU_7
from .symbols.SymbolU_3V3_2 import SymbolU_3V3
from .symbols.SymbolU_5V_1 import SymbolU_5V
class Power_1(Circuit):
    GND_1 = Port()
    U_3V3 = Port()
    U_5V = Port()

    C1 = CL21A106KAYNNNE.Device()
    C2 = CL05F104ZO5NNNC.Device()
    C4 = CL05F104ZO5NNNC.Device()
    C6 = comma_ai_11112255_C0402.Device()
    C7 = CL05F104ZO5NNNC.Device()
    C8 = CL21A106KAYNNNE.Device()
    L1 = MEKK2520T3R3M.Device()
    R1 = RC0402FR_0710KL.Device()
    R3 = RC0402FR_0710KL.Device()
    R4 = RC0402JR_07100KL.Device()
    R5 = RC0402JR_07100KL.Device()
    R6 = RC0402JR_07100KL.Device()
    U1 = AP62300WU_7.Device()

    nets = [
        Net([C4.p[1], U1.BST], name="Net_U1_BST"),
        Net([R1.p[2], U1.EN], name="Net_U1_EN"),
        Net([C6.p[1], R3.p[1], R4.p[2], R5.p[2], R6.p[2], U1.FB], name="Net_U1_FB"),
        Net([C4.p[2], L1.p[1], U1.SW], name="Net_U1_SW"),
        Net([GND_1, C1.p[2], C2.p[2], C7.p[2], C8.p[2], R3.p[2], U1.GND], name="GND"),
        Net([U_3V3, C6.p[2], C7.p[1], C8.p[1], L1.p[2], R4.p[1], R5.p[1], R6.p[1]], name="Net3V3", symbol=SymbolU_3V3()),
        Net([U_5V, C1.p[1], C2.p[1], R1.p[1], U1.IN], name="Net5V", symbol=SymbolU_5V()),
    ]

    def __init__(self):
        self.place(self.C1, Transform((51.6251, 47.1365)))
        self.place(self.C2, Transform((0, 63.1065)))
        self.place(self.C4, Transform((0, 61.0795)))
        self.place(self.C6, Transform((0, 57.0255)))
        self.place(self.C7, Transform((0, 54.9985)))
        self.place(self.C8, Transform((51.6251, 41.6825)))
        self.place(self.L1, Transform((0.6651, 2.2065)))
        self.place(self.R1, Transform((5.9936, 42.8365)))
        self.place(self.R3, Transform((5.9936, 38.7825)))
        self.place(self.R4, Transform((5.9936, 36.7555)))
        self.place(self.R5, Transform((5.9936, 34.7285)))
        self.place(self.R6, Transform((8.9904, 63.1065)))
        self.place(self.U1, Transform((61.7108, 0)))

        self.C6.x_out = True


from .components.UNKNOWN import comma_ai_11112255_C0402 as comma_ai_11112255_C0402
from .components.UNKNOWN import CL05F104ZO5NNNC as CL05F104ZO5NNNC
from .components.UNKNOWN import CL21A106KAYNNNE as CL21A106KAYNNNE
from .components.UNKNOWN import SMAJ16CA_13_F as SMAJ16CA_13_F
from .components.UNKNOWN import PMEG10020ELRX as PMEG10020ELRX
from .components.UNKNOWN import PJ_002AH_SMT_TR as PJ_002AH_SMT_TR
from .components.UNKNOWN import MEKK2520T3R3M as MEKK2520T3R3M
from .components.UNKNOWN import SI7101DN_T1_GE3 as SI7101DN_T1_GE3
from .components.UNKNOWN import RC0402FR_0752K3L as RC0402FR_0752K3L
from .components.UNKNOWN import RC0402JR_071KL as RC0402JR_071KL
from .components.UNKNOWN import RC0402FR_0710KL as RC0402FR_0710KL
from .components.UNKNOWN import AP62300WU_7 as AP62300WU_7
from .symbols.SymbolU_12V_2 import SymbolU_12V
from .symbols.SymbolU_5V_1 import SymbolU_5V
class Power_2(Circuit):
    GND_1 = Port()
    U_12V = Port()
    U_5V = Port()

    C10 = comma_ai_11112255_C0402.Device()
    C11 = CL05F104ZO5NNNC.Device()
    C12 = CL21A106KAYNNNE.Device()
    C13 = CL21A106KAYNNNE.Device()
    C3 = CL21A106KAYNNNE.Device()
    C5 = CL05F104ZO5NNNC.Device()
    C9 = CL05F104ZO5NNNC.Device()
    D1 = SMAJ16CA_13_F.Device()
    D2 = PMEG10020ELRX.Device()
    J1 = PJ_002AH_SMT_TR.Device()
    L2 = MEKK2520T3R3M.Device()
    Q1 = SI7101DN_T1_GE3.Device()
    R10 = RC0402FR_0752K3L.Device()
    R2 = RC0402JR_071KL.Device()
    R7 = RC0402FR_0710KL.Device()
    R8 = RC0402FR_0710KL.Device()
    R9 = RC0402FR_0710KL.Device()
    U2 = AP62300WU_7.Device()

    nets = [
        Net([D2.A, Q1.G, R2.p[2]], name="Net_D2_A"),
        Net([D1.p[2], J1.PWR, Q1.D], name="Net_J1_PWR"),
        Net([C9.p[1], U2.BST], name="Net_U2_BST"),
        Net([R7.p[2], R8.p[1], U2.EN], name="Net_U2_EN"),
        Net([C10.p[1], R10.p[1], R9.p[1], U2.FB], name="Net_U2_FB"),
        Net([C9.p[2], L2.p[1], U2.SW], name="Net_U2_SW"),
        Net([GND_1, C11.p[2], C12.p[2], C13.p[2], C3.p[2], C5.p[2], D1.p[1], J1.GND, J1.GNDBREAK, R2.p[1], R8.p[2], R9.p[2], U2.GND], name="GND"),
        Net([U_12V, C3.p[1], C5.p[1], D2.C, Q1.S, R7.p[1], U2.IN], name="Net12V", symbol=SymbolU_12V()),
        Net([U_5V, C10.p[2], C11.p[1], C12.p[1], C13.p[1], L2.p[2], R10.p[2]], name="Net5V", symbol=SymbolU_5V()),
    ]

    def __init__(self):
        self.place(self.C10, Transform((0, 52.265)))
        self.place(self.C11, Transform((0, 50.238)))
        self.place(self.C12, Transform((51.6251, 40.276)))
        self.place(self.C13, Transform((51.6251, 37.549)))
        self.place(self.C3, Transform((51.6251, 45.73)))
        self.place(self.C5, Transform((0, 60.373)))
        self.place(self.C9, Transform((0, 54.292)))
        self.place(self.D1, Transform((31.844, 3.0843)))
        self.place(self.D2, Transform((9.2911, 2.8655)))
        self.place(self.J1, Transform((44.0278, 18.4405)))
        self.place(self.L2, Transform((0.6651, 0)))
        self.place(self.Q1, Transform((5.3091, 3.0643)))
        self.place(self.R10, Transform((8.9904, 56.319)))
        self.place(self.R2, Transform((5.9936, 42.13)))
        self.place(self.R7, Transform((8.9904, 62.4)))
        self.place(self.R8, Transform((8.9904, 60.373)))
        self.place(self.R9, Transform((8.9904, 58.346)))
        self.place(self.U2, Transform((65.7082, 1.3205)))

        self.C10.x_out = True


from .components.UNKNOWN import comma_ai_11112255_M2_BOLT as comma_ai_11112255_M2_BOLT
class Power_3(Circuit):
    GND_1 = Port()

    BH4 = comma_ai_11112255_M2_BOLT.Device()

    nets = [
        Net([GND_1, BH4.p[1]], name="GND"),
    ]

    def __init__(self):
        self.place(self.BH4, Transform((0, 0)))

        self.BH4.x_out = True


from .components.UNKNOWN import comma_ai_11112255_M2_BOLT as comma_ai_11112255_M2_BOLT
class Power_4(Circuit):
    GND_1 = Port()

    BH3 = comma_ai_11112255_M2_BOLT.Device()

    nets = [
        Net([GND_1, BH3.p[1]], name="GND"),
    ]

    def __init__(self):
        self.place(self.BH3, Transform((0, 0)))

        self.BH3.x_out = True


from .components.UNKNOWN import comma_ai_11112255_M2_BOLT as comma_ai_11112255_M2_BOLT
class Power_5(Circuit):
    GND_1 = Port()

    BH2 = comma_ai_11112255_M2_BOLT.Device()

    nets = [
        Net([GND_1, BH2.p[1]], name="GND"),
    ]

    def __init__(self):
        self.place(self.BH2, Transform((0, 0)))

        self.BH2.x_out = True


from .components.UNKNOWN import comma_ai_11112255_M2_BOLT as comma_ai_11112255_M2_BOLT
class Power_6(Circuit):
    GND_1 = Port()

    BH1 = comma_ai_11112255_M2_BOLT.Device()

    nets = [
        Net([GND_1, BH1.p[1]], name="GND"),
    ]

    def __init__(self):
        self.place(self.BH1, Transform((0, 0)))

        self.BH1.x_out = True


from .symbols.SymbolU_5V_1 import SymbolU_5V
from .symbols.SymbolU_3V3_2 import SymbolU_3V3
from .symbols.SymbolU_12V_2 import SymbolU_12V
class Power(Circuit):
    GND_1 = Port()
    U_12V = Port()
    U_3V3 = Port()
    U_5V = Port()

    Power_1 = Power_1()
    Power_2 = Power_2()
    Power_3 = Power_3()
    Power_4 = Power_4()
    Power_5 = Power_5()
    Power_6 = Power_6()

    nets = [
        Net([GND_1, Power_1.GND_1, Power_2.GND_1, Power_3.GND_1, Power_4.GND_1, Power_5.GND_1, Power_6.GND_1], name="GND"),
        Net([U_12V, Power_2.U_12V], name="Net12V", symbol=SymbolU_12V()),
        Net([U_3V3, Power_1.U_3V3], name="Net3V3", symbol=SymbolU_3V3()),
        Net([U_5V, Power_1.U_5V, Power_2.U_5V], name="Net5V", symbol=SymbolU_5V()),
    ]

    def __init__(self):
        self.place(self.Power_1, Transform((0, 1.3205)))
        self.place(self.Power_2, Transform((0, 0)))
        self.place(self.Power_3, Transform((25.4516, 16.8405)))
        self.place(self.Power_4, Transform((25.4516, 22.0405)))
        self.place(self.Power_5, Transform((25.4516, 27.2405)))
        self.place(self.Power_6, Transform((25.4516, 32.4405)))


from .components.UNKNOWN import CL05F104ZO5NNNC as CL05F104ZO5NNNC
from .components.UNKNOWN import MH1608_601Y as MH1608_601Y
from .symbols.SymbolU_3V3_2 import SymbolU_3V3
class Pcbgolf_2_1(Circuit):
    GND_1 = Port()
    U_3V3 = Port()
    VDDA_1 = Port()

    C22 = CL05F104ZO5NNNC.Device()
    L3 = MH1608_601Y.Device()

    nets = [
        Net([GND_1, C22.p[2]], name="GND"),
        Net([U_3V3, L3.p[1]], name="Net3V3", symbol=SymbolU_3V3()),
        Net([VDDA_1, C22.p[1], L3.p[2]], name="VDDA"),
    ]

    def __init__(self):
        self.place(self.C22, Transform((0, 36.3209)))
        self.place(self.L3, Transform((12.7651, 0)))



from .components.UNKNOWN import C0402C120J5GACTU as C0402C120J5GACTU
from .components.UNKNOWN import CL21A106KAYNNNE as CL21A106KAYNNNE
from .components.UNKNOWN import CL05F104ZO5NNNC as CL05F104ZO5NNNC
from .components.UNKNOWN import RC0402FR_0710KL as RC0402FR_0710KL
from .components.UNKNOWN import RC0402JR_07100KL as RC0402JR_07100KL
from .components.UNKNOWN import STM32H725ZGT as STM32H725ZGT
from .components.UNKNOWN import RH100_25_000_12_F_1010_TR as RH100_25_000_12_F_1010_TR
from .symbols.SymbolU_3V3_2 import SymbolU_3V3
class Pcbgolf_2_2(Circuit):
    BTN_1 = Port()
    CAN0_EN_1 = Port()
    CAN0_RX_1 = Port()
    CAN0_TX_1 = Port()
    CAN1_EN_1 = Port()
    CAN1_RX_1 = Port()
    CAN1_TX_1 = Port()
    CAN2_EN_1 = Port()
    CAN2_RX_1 = Port()
    CAN2_TX_1 = Port()
    CAN3_EN_1 = Port()
    CAN3_RX_1 = Port()
    CAN3_TX_1 = Port()
    CH1_IMON_1 = Port()
    CH1_PWR_EN_1 = Port()
    CH1_SBU1_1 = Port()
    CH1_SBU1_IGN_1 = Port()
    CH1_SBU1_RELAY_1 = Port()
    CH1_SBU2_1 = Port()
    CH1_SBU2_IGN_1 = Port()
    CH1_SBU2_RELAY_1 = Port()
    CH2_IMON_1 = Port()
    CH2_PWR_EN_1 = Port()
    CH2_SBU1_1 = Port()
    CH2_SBU1_IGN_1 = Port()
    CH2_SBU1_RELAY_1 = Port()
    CH2_SBU2_1 = Port()
    CH2_SBU2_IGN_1 = Port()
    CH2_SBU2_RELAY_1 = Port()
    CH3_IMON_1 = Port()
    CH3_PWR_EN_1 = Port()
    CH3_SBU1_1 = Port()
    CH3_SBU1_IGN_1 = Port()
    CH3_SBU1_RELAY_1 = Port()
    CH3_SBU2_1 = Port()
    CH3_SBU2_IGN_1 = Port()
    CH3_SBU2_RELAY_1 = Port()
    CH4_IMON_1 = Port()
    CH4_PWR_EN_1 = Port()
    CH4_SBU1_1 = Port()
    CH4_SBU1_IGN_1 = Port()
    CH4_SBU1_RELAY_1 = Port()
    CH4_SBU2_1 = Port()
    CH4_SBU2_IGN_1 = Port()
    CH4_SBU2_RELAY_1 = Port()
    GND_1 = Port()
    HUB_SCL_1 = Port()
    HUB_SDA_1 = Port()
    LED_B_1 = Port()
    LED_G_1 = Port()
    LED_R_1 = Port()
    SD_CLK_1 = Port()
    SD_CMD_1 = Port()
    SD_D0_1 = Port()
    SD_D1_1 = Port()
    SD_D2_1 = Port()
    SD_D3_1 = Port()
    STM_D_N_1 = Port()
    STM_D_P_1 = Port()
    U_3V3 = Port()
    VDDA_1 = Port()
    VDDLDO_1 = Port()
    VLXSMPS_1 = Port()

    C14 = C0402C120J5GACTU.Device()
    C15 = CL21A106KAYNNNE.Device()
    C16 = CL05F104ZO5NNNC.Device()
    C17 = C0402C120J5GACTU.Device()
    C18 = CL05F104ZO5NNNC.Device()
    R11 = RC0402FR_0710KL.Device()
    R12 = RC0402FR_0710KL.Device()
    R13 = RC0402JR_07100KL.Device()
    R14 = RC0402JR_07100KL.Device()
    R15 = RC0402JR_07100KL.Device()
    R16 = RC0402JR_07100KL.Device()
    R17 = RC0402JR_07100KL.Device()
    R18 = RC0402JR_07100KL.Device()
    R19 = RC0402JR_07100KL.Device()
    R20 = RC0402JR_07100KL.Device()
    U3 = STM32H725ZGT.Device()
    Y1 = RH100_25_000_12_F_1010_TR.Device()

    nets = [
        Net([R17.p[1], U3.PC0], name="Net_U3_PC0"),
        Net([R18.p[1], U3.PC1], name="Net_U3_PC1"),
        Net([R19.p[1], U3.PC2_C], name="Net_U3_PC2_C"),
        Net([R20.p[1], U3.PC3_C], name="Net_U3_PC3_C"),
        Net([R11.p[2], U3.PDR_ON], name="Net_U3_PDR_ON"),
        Net([R16.p[1], U3.PF10], name="Net_U3_PF10"),
        Net([R13.p[1], U3.PF7], name="Net_U3_PF7"),
        Net([R14.p[1], U3.PF8], name="Net_U3_PF8"),
        Net([R15.p[1], U3.PF9], name="Net_U3_PF9"),
        Net([C14.p[1], U3.PH0, Y1.p[1]], name="Net_U3_PH0"),
        Net([C17.p[1], U3.PH1, Y1.p[2]], name="Net_U3_PH1"),
        Net([BTN_1, R12.p[2], U3.BOOT0, U3.PE15], name="BTN"),
        Net([CAN0_EN_1, U3.PB7], name="CAN0_EN"),
        Net([CAN0_RX_1, U3.PB8], name="CAN0_RX"),
        Net([CAN0_TX_1, U3.PB9], name="CAN0_TX"),
        Net([CAN1_EN_1, U3.PB3JTDO], name="CAN1_EN"),
        Net([CAN1_RX_1, U3.PB5], name="CAN1_RX"),
        Net([CAN1_TX_1, U3.PB6], name="CAN1_TX"),
        Net([CAN2_EN_1, U3.PD7], name="CAN2_EN"),
        Net([CAN2_RX_1, U3.PG10], name="CAN2_RX"),
        Net([CAN2_TX_1, U3.PG9], name="CAN2_TX"),
        Net([CAN3_EN_1, U3.PB4NJTRST], name="CAN3_EN"),
        Net([CAN3_RX_1, U3.PB12], name="CAN3_RX"),
        Net([CAN3_TX_1, U3.PB13], name="CAN3_TX"),
        Net([CH1_IMON_1, U3.PC4], name="CH1_IMON"),
        Net([CH1_PWR_EN_1, U3.PA0], name="CH1_PWR_EN"),
        Net([CH1_SBU1_1, R19.p[2]], name="CH1_SBU1"),
        Net([CH1_SBU1_IGN_1, U3.PD0], name="CH1_SBU1_IGN"),
        Net([CH1_SBU1_RELAY_1, U3.PD1], name="CH1_SBU1_RELAY"),
        Net([CH1_SBU2_1, R20.p[2]], name="CH1_SBU2"),
        Net([CH1_SBU2_IGN_1, U3.PD3], name="CH1_SBU2_IGN"),
        Net([CH1_SBU2_RELAY_1, U3.PD4], name="CH1_SBU2_RELAY"),
        Net([CH2_IMON_1, U3.PB1], name="CH2_IMON"),
        Net([CH2_PWR_EN_1, U3.PA1], name="CH2_PWR_EN"),
        Net([CH2_SBU1_1, R15.p[2]], name="CH2_SBU1"),
        Net([CH2_SBU1_IGN_1, U3.PD5], name="CH2_SBU1_IGN"),
        Net([CH2_SBU1_RELAY_1, U3.PD6], name="CH2_SBU1_RELAY"),
        Net([CH2_SBU2_1, R13.p[2]], name="CH2_SBU2"),
        Net([CH2_SBU2_IGN_1, U3.PD8], name="CH2_SBU2_IGN"),
        Net([CH2_SBU2_RELAY_1, U3.PD10], name="CH2_SBU2_RELAY"),
        Net([CH3_IMON_1, U3.PF11], name="CH3_IMON"),
        Net([CH3_PWR_EN_1, U3.PA4], name="CH3_PWR_EN"),
        Net([CH3_SBU1_1, R17.p[2]], name="CH3_SBU1"),
        Net([CH3_SBU1_IGN_1, U3.PD12], name="CH3_SBU1_IGN"),
        Net([CH3_SBU1_RELAY_1, U3.PD11], name="CH3_SBU1_RELAY"),
        Net([CH3_SBU2_1, R18.p[2]], name="CH3_SBU2"),
        Net([CH3_SBU2_IGN_1, U3.PD9], name="CH3_SBU2_IGN"),
        Net([CH3_SBU2_RELAY_1, U3.PD13], name="CH3_SBU2_RELAY"),
        Net([CH4_IMON_1, U3.PA6], name="CH4_IMON"),
        Net([CH4_PWR_EN_1, U3.PA5], name="CH4_PWR_EN"),
        Net([CH4_SBU1_1, R16.p[2]], name="CH4_SBU1"),
        Net([CH4_SBU1_IGN_1, U3.PD14], name="CH4_SBU1_IGN"),
        Net([CH4_SBU1_RELAY_1, U3.PD15], name="CH4_SBU1_RELAY"),
        Net([CH4_SBU2_1, R14.p[2]], name="CH4_SBU2"),
        Net([CH4_SBU2_IGN_1, U3.PE0], name="CH4_SBU2_IGN"),
        Net([CH4_SBU2_RELAY_1, U3.PE1], name="CH4_SBU2_RELAY"),
        Net([GND_1, C14.p[2], C15.p[2], C16.p[2], C17.p[2], C18.p[2], R12.p[1], U3.VSS, U3.VSSA, U3.VSSSMPS, Y1.p[3]], name="GND"),
        Net([HUB_SCL_1, U3.PB10], name="HUB_SCL"),
        Net([HUB_SDA_1, U3.PB11], name="HUB_SDA"),
        Net([LED_B_1, U3.PE2], name="LED_B"),
        Net([LED_G_1, U3.PE3], name="LED_G"),
        Net([LED_R_1, U3.PE4], name="LED_R"),
        Net([U_3V3, R11.p[1], U3.VBAT, U3.VDD[0], U3.VDD[1], U3.VDD[2], U3.VDD[3], U3.VDD[4], U3.VDD[5], U3.VDD[6], U3.VDD[7], U3.VDD[8], U3.VDD[9], U3.VDD[10], U3.VDD[11], U3.VDD[12], U3.VDD33USB, U3.VDD50USB, U3.VDDSMPS], name="Net3V3", symbol=SymbolU_3V3()),
        Net([SD_CLK_1, U3.PC12], name="SD_CLK"),
        Net([SD_CMD_1, U3.PD2], name="SD_CMD"),
        Net([SD_D0_1, U3.PC8], name="SD_D0"),
        Net([SD_D1_1, U3.PC9], name="SD_D1"),
        Net([SD_D2_1, U3.PC10], name="SD_D2"),
        Net([SD_D3_1, U3.PC11], name="SD_D3"),
        Net([STM_D_N_1, U3.PA11], name="STM_D_N"),
        Net([STM_D_P_1, U3.PA12], name="STM_D_P"),
        Net([VDDA_1, U3.VDDA, U3.VREFp], name="VDDA"),
        Net([VDDLDO_1, C15.p[1], C16.p[1], C18.p[1], U3.VCAP[0], U3.VCAP[1], U3.VCAP[2], U3.VDDLDO[0], U3.VDDLDO[1], U3.VDDLDO[2], U3.VFBSMPS], name="VDDLDO"),
        Net([VLXSMPS_1, U3.VLXSMPS], name="VLXSMPS"),
    ]

    def __init__(self):
        self.place(self.C14, Transform((0, 38.6705)))
        self.place(self.C15, Transform((55.7521, 38.9165)))
        self.place(self.C16, Transform((0, 36.6435)))
        self.place(self.C17, Transform((0, 34.6165)))
        self.place(self.C18, Transform((0, 32.5895)))
        self.place(self.R11, Transform((8.9904, 44.7515)))
        self.place(self.R12, Transform((8.9904, 42.7245)))
        self.place(self.R13, Transform((8.9904, 40.6975)))
        self.place(self.R14, Transform((8.9904, 38.6705)))
        self.place(self.R15, Transform((8.9904, 36.6435)))
        self.place(self.R16, Transform((8.9904, 34.6165)))
        self.place(self.R17, Transform((8.9904, 32.5895)))
        self.place(self.R18, Transform((8.9904, 30.5625)))
        self.place(self.R19, Transform((8.9904, 28.5355)))
        self.place(self.R20, Transform((-3.0, 7.075), rotate=180))
        self.place(self.U3, Transform((10.6766, 13.325)))
        self.place(self.Y1, Transform((62.4251, 0)))



from .components.UNKNOWN import EVQ_Q2Y03W as EVQ_Q2Y03W
from .symbols.SymbolU_3V3_2 import SymbolU_3V3
class Pcbgolf_2_3(Circuit):
    BTN_1 = Port()
    U_3V3 = Port()

    SW1 = EVQ_Q2Y03W.Device()

    nets = [
        Net([BTN_1, SW1.P, SW1.P1], name="BTN"),
        Net([U_3V3, SW1.S, SW1.S1], name="Net3V3", symbol=SymbolU_3V3()),
    ]

    def __init__(self):
        self.place(self.SW1, Transform((0, 0)))



from .components.UNKNOWN import CL21A106KAYNNNE as CL21A106KAYNNNE
from .components.UNKNOWN import CL05F104ZO5NNNC as CL05F104ZO5NNNC
from .symbols.SymbolU_3V3_2 import SymbolU_3V3
class Pcbgolf_2_4(Circuit):
    GND_1 = Port()
    U_3V3 = Port()

    C19 = CL21A106KAYNNNE.Device()
    C20 = CL21A106KAYNNNE.Device()
    C23 = CL05F104ZO5NNNC.Device()
    C24 = CL05F104ZO5NNNC.Device()
    C26 = CL05F104ZO5NNNC.Device()
    C27 = CL05F104ZO5NNNC.Device()

    nets = [
        Net([GND_1, C19.p[2], C20.p[2], C23.p[2], C24.p[2], C26.p[2], C27.p[2]], name="GND"),
        Net([U_3V3, C19.p[1], C20.p[1], C23.p[1], C24.p[1], C26.p[1], C27.p[1]], name="Net3V3", symbol=SymbolU_3V3()),
    ]

    def __init__(self):
        self.place(self.C19, Transform((55.7521, 9.681)))
        self.place(self.C20, Transform((55.7521, 6.954)))
        self.place(self.C23, Transform((0, 2.027)))
        self.place(self.C24, Transform((0, 0)))
        self.place(self.C26, Transform((2.9968, 26.351)))
        self.place(self.C27, Transform((2.9968, 24.324)))



from .components.UNKNOWN import CL21A106KAYNNNE as CL21A106KAYNNNE
from .components.UNKNOWN import Comp_04025A221FAT2A as Comp_04025A221FAT2A
from .components.UNKNOWN import LQM2MPN2R2NG0L as LQM2MPN2R2NG0L
class Pcbgolf_2_5(Circuit):
    GND_1 = Port()
    VDDLDO_1 = Port()
    VLXSMPS_1 = Port()

    C21 = CL21A106KAYNNNE.Device()
    C25 = Comp_04025A221FAT2A.Device()
    L4 = LQM2MPN2R2NG0L.Device()

    nets = [
        Net([GND_1, C21.p[2], C25.p[2]], name="GND"),
        Net([VDDLDO_1, C21.p[1], L4.p[1]], name="VDDLDO"),
        Net([VLXSMPS_1, C25.p[1], L4.p[2]], name="VLXSMPS"),
    ]

    def __init__(self):
        self.place(self.C21, Transform((52.7553, 39.613)))
        self.place(self.C25, Transform((0, 63.764)))
        self.place(self.L4, Transform((9.7183, 0)))



from .components.UNKNOWN import CLMVC_FKA_CL1D1L71BB7C3C3 as CLMVC_FKA_CL1D1L71BB7C3C3
from .components.UNKNOWN import RC0402JR_071KL as RC0402JR_071KL
from .components.UNKNOWN import RC0402JR_072K7L as RC0402JR_072K7L
from .symbols.SymbolU_3V3_2 import SymbolU_3V3
class Pcbgolf_2_6(Circuit):
    LED_B_1 = Port()
    LED_G_1 = Port()
    LED_R_1 = Port()
    U_3V3 = Port()

    LED1 = CLMVC_FKA_CL1D1L71BB7C3C3.Device()
    R21 = RC0402JR_071KL.Device()
    R22 = RC0402JR_072K7L.Device()
    R23 = RC0402JR_071KL.Device()

    nets = [
        Net([LED1.Bn, R23.p[1]], name="Net_LED1_B_"),
        Net([LED1.Gn, R22.p[1]], name="Net_LED1_G_"),
        Net([LED1.Rn, R21.p[1]], name="Net_LED1_R_"),
        Net([LED_B_1, R23.p[2]], name="LED_B"),
        Net([LED_G_1, R22.p[2]], name="LED_G"),
        Net([LED_R_1, R21.p[2]], name="LED_R"),
        Net([U_3V3, LED1.COMp], name="Net3V3", symbol=SymbolU_3V3()),
    ]

    def __init__(self):
        self.place(self.LED1, Transform((4.8179, 0)))
        self.place(self.R21, Transform((0, 60.92)))
        self.place(self.R22, Transform((0, 58.893)))
        self.place(self.R23, Transform((0, 56.866)))



from .symbols.SymbolU_3V3_2 import SymbolU_3V3
class Pcbgolf_2(Circuit):
    CAN0_EN_1 = Port()
    CAN0_RX_1 = Port()
    CAN0_TX_1 = Port()
    CAN1_EN_1 = Port()
    CAN1_RX_1 = Port()
    CAN1_TX_1 = Port()
    CAN2_EN_1 = Port()
    CAN2_RX_1 = Port()
    CAN2_TX_1 = Port()
    CAN3_EN_1 = Port()
    CAN3_RX_1 = Port()
    CAN3_TX_1 = Port()
    CH1_IMON_1 = Port()
    CH1_PWR_EN_1 = Port()
    CH1_SBU1_1 = Port()
    CH1_SBU1_IGN_1 = Port()
    CH1_SBU1_RELAY_1 = Port()
    CH1_SBU2_1 = Port()
    CH1_SBU2_IGN_1 = Port()
    CH1_SBU2_RELAY_1 = Port()
    CH2_IMON_1 = Port()
    CH2_PWR_EN_1 = Port()
    CH2_SBU1_1 = Port()
    CH2_SBU1_IGN_1 = Port()
    CH2_SBU1_RELAY_1 = Port()
    CH2_SBU2_1 = Port()
    CH2_SBU2_IGN_1 = Port()
    CH2_SBU2_RELAY_1 = Port()
    CH3_IMON_1 = Port()
    CH3_PWR_EN_1 = Port()
    CH3_SBU1_1 = Port()
    CH3_SBU1_IGN_1 = Port()
    CH3_SBU1_RELAY_1 = Port()
    CH3_SBU2_1 = Port()
    CH3_SBU2_IGN_1 = Port()
    CH3_SBU2_RELAY_1 = Port()
    CH4_IMON_1 = Port()
    CH4_PWR_EN_1 = Port()
    CH4_SBU1_1 = Port()
    CH4_SBU1_IGN_1 = Port()
    CH4_SBU1_RELAY_1 = Port()
    CH4_SBU2_1 = Port()
    CH4_SBU2_IGN_1 = Port()
    CH4_SBU2_RELAY_1 = Port()
    GND_1 = Port()
    HUB_SCL_1 = Port()
    HUB_SDA_1 = Port()
    SD_CLK_1 = Port()
    SD_CMD_1 = Port()
    SD_D0_1 = Port()
    SD_D1_1 = Port()
    SD_D2_1 = Port()
    SD_D3_1 = Port()
    STM_D_N_1 = Port()
    STM_D_P_1 = Port()
    U_3V3 = Port()

    Pcbgolf_2_1 = Pcbgolf_2_1()
    Pcbgolf_2_2 = Pcbgolf_2_2()
    Pcbgolf_2_3 = Pcbgolf_2_3()
    Pcbgolf_2_4 = Pcbgolf_2_4()
    Pcbgolf_2_5 = Pcbgolf_2_5()
    Pcbgolf_2_6 = Pcbgolf_2_6()

    nets = [
        Net([Pcbgolf_2_2.BTN_1, Pcbgolf_2_3.BTN_1], name="BTN"),
        Net([Pcbgolf_2_2.LED_B_1, Pcbgolf_2_6.LED_B_1], name="LED_B"),
        Net([Pcbgolf_2_2.LED_G_1, Pcbgolf_2_6.LED_G_1], name="LED_G"),
        Net([Pcbgolf_2_2.LED_R_1, Pcbgolf_2_6.LED_R_1], name="LED_R"),
        Net([Pcbgolf_2_1.VDDA_1, Pcbgolf_2_2.VDDA_1], name="VDDA"),
        Net([Pcbgolf_2_2.VDDLDO_1, Pcbgolf_2_5.VDDLDO_1], name="VDDLDO"),
        Net([Pcbgolf_2_2.VLXSMPS_1, Pcbgolf_2_5.VLXSMPS_1], name="VLXSMPS"),
        Net([CAN0_EN_1, Pcbgolf_2_2.CAN0_EN_1], name="CAN0_EN"),
        Net([CAN0_RX_1, Pcbgolf_2_2.CAN0_RX_1], name="CAN0_RX"),
        Net([CAN0_TX_1, Pcbgolf_2_2.CAN0_TX_1], name="CAN0_TX"),
        Net([CAN1_EN_1, Pcbgolf_2_2.CAN1_EN_1], name="CAN1_EN"),
        Net([CAN1_RX_1, Pcbgolf_2_2.CAN1_RX_1], name="CAN1_RX"),
        Net([CAN1_TX_1, Pcbgolf_2_2.CAN1_TX_1], name="CAN1_TX"),
        Net([CAN2_EN_1, Pcbgolf_2_2.CAN2_EN_1], name="CAN2_EN"),
        Net([CAN2_RX_1, Pcbgolf_2_2.CAN2_RX_1], name="CAN2_RX"),
        Net([CAN2_TX_1, Pcbgolf_2_2.CAN2_TX_1], name="CAN2_TX"),
        Net([CAN3_EN_1, Pcbgolf_2_2.CAN3_EN_1], name="CAN3_EN"),
        Net([CAN3_RX_1, Pcbgolf_2_2.CAN3_RX_1], name="CAN3_RX"),
        Net([CAN3_TX_1, Pcbgolf_2_2.CAN3_TX_1], name="CAN3_TX"),
        Net([CH1_IMON_1, Pcbgolf_2_2.CH1_IMON_1], name="CH1_IMON"),
        Net([CH1_PWR_EN_1, Pcbgolf_2_2.CH1_PWR_EN_1], name="CH1_PWR_EN"),
        Net([CH1_SBU1_1, Pcbgolf_2_2.CH1_SBU1_1], name="CH1_SBU1"),
        Net([CH1_SBU1_IGN_1, Pcbgolf_2_2.CH1_SBU1_IGN_1], name="CH1_SBU1_IGN"),
        Net([CH1_SBU1_RELAY_1, Pcbgolf_2_2.CH1_SBU1_RELAY_1], name="CH1_SBU1_RELAY"),
        Net([CH1_SBU2_1, Pcbgolf_2_2.CH1_SBU2_1], name="CH1_SBU2"),
        Net([CH1_SBU2_IGN_1, Pcbgolf_2_2.CH1_SBU2_IGN_1], name="CH1_SBU2_IGN"),
        Net([CH1_SBU2_RELAY_1, Pcbgolf_2_2.CH1_SBU2_RELAY_1], name="CH1_SBU2_RELAY"),
        Net([CH2_IMON_1, Pcbgolf_2_2.CH2_IMON_1], name="CH2_IMON"),
        Net([CH2_PWR_EN_1, Pcbgolf_2_2.CH2_PWR_EN_1], name="CH2_PWR_EN"),
        Net([CH2_SBU1_1, Pcbgolf_2_2.CH2_SBU1_1], name="CH2_SBU1"),
        Net([CH2_SBU1_IGN_1, Pcbgolf_2_2.CH2_SBU1_IGN_1], name="CH2_SBU1_IGN"),
        Net([CH2_SBU1_RELAY_1, Pcbgolf_2_2.CH2_SBU1_RELAY_1], name="CH2_SBU1_RELAY"),
        Net([CH2_SBU2_1, Pcbgolf_2_2.CH2_SBU2_1], name="CH2_SBU2"),
        Net([CH2_SBU2_IGN_1, Pcbgolf_2_2.CH2_SBU2_IGN_1], name="CH2_SBU2_IGN"),
        Net([CH2_SBU2_RELAY_1, Pcbgolf_2_2.CH2_SBU2_RELAY_1], name="CH2_SBU2_RELAY"),
        Net([CH3_IMON_1, Pcbgolf_2_2.CH3_IMON_1], name="CH3_IMON"),
        Net([CH3_PWR_EN_1, Pcbgolf_2_2.CH3_PWR_EN_1], name="CH3_PWR_EN"),
        Net([CH3_SBU1_1, Pcbgolf_2_2.CH3_SBU1_1], name="CH3_SBU1"),
        Net([CH3_SBU1_IGN_1, Pcbgolf_2_2.CH3_SBU1_IGN_1], name="CH3_SBU1_IGN"),
        Net([CH3_SBU1_RELAY_1, Pcbgolf_2_2.CH3_SBU1_RELAY_1], name="CH3_SBU1_RELAY"),
        Net([CH3_SBU2_1, Pcbgolf_2_2.CH3_SBU2_1], name="CH3_SBU2"),
        Net([CH3_SBU2_IGN_1, Pcbgolf_2_2.CH3_SBU2_IGN_1], name="CH3_SBU2_IGN"),
        Net([CH3_SBU2_RELAY_1, Pcbgolf_2_2.CH3_SBU2_RELAY_1], name="CH3_SBU2_RELAY"),
        Net([CH4_IMON_1, Pcbgolf_2_2.CH4_IMON_1], name="CH4_IMON"),
        Net([CH4_PWR_EN_1, Pcbgolf_2_2.CH4_PWR_EN_1], name="CH4_PWR_EN"),
        Net([CH4_SBU1_1, Pcbgolf_2_2.CH4_SBU1_1], name="CH4_SBU1"),
        Net([CH4_SBU1_IGN_1, Pcbgolf_2_2.CH4_SBU1_IGN_1], name="CH4_SBU1_IGN"),
        Net([CH4_SBU1_RELAY_1, Pcbgolf_2_2.CH4_SBU1_RELAY_1], name="CH4_SBU1_RELAY"),
        Net([CH4_SBU2_1, Pcbgolf_2_2.CH4_SBU2_1], name="CH4_SBU2"),
        Net([CH4_SBU2_IGN_1, Pcbgolf_2_2.CH4_SBU2_IGN_1], name="CH4_SBU2_IGN"),
        Net([CH4_SBU2_RELAY_1, Pcbgolf_2_2.CH4_SBU2_RELAY_1], name="CH4_SBU2_RELAY"),
        Net([GND_1, Pcbgolf_2_1.GND_1, Pcbgolf_2_2.GND_1, Pcbgolf_2_4.GND_1, Pcbgolf_2_5.GND_1], name="GND"),
        Net([HUB_SCL_1, Pcbgolf_2_2.HUB_SCL_1], name="HUB_SCL"),
        Net([HUB_SDA_1, Pcbgolf_2_2.HUB_SDA_1], name="HUB_SDA"),
        Net([U_3V3, Pcbgolf_2_1.U_3V3, Pcbgolf_2_2.U_3V3, Pcbgolf_2_3.U_3V3, Pcbgolf_2_4.U_3V3, Pcbgolf_2_6.U_3V3], name="Net3V3", symbol=SymbolU_3V3()),
        Net([SD_CLK_1, Pcbgolf_2_2.SD_CLK_1], name="SD_CLK"),
        Net([SD_CMD_1, Pcbgolf_2_2.SD_CMD_1], name="SD_CMD"),
        Net([SD_D0_1, Pcbgolf_2_2.SD_D0_1], name="SD_D0"),
        Net([SD_D1_1, Pcbgolf_2_2.SD_D1_1], name="SD_D1"),
        Net([SD_D2_1, Pcbgolf_2_2.SD_D2_1], name="SD_D2"),
        Net([SD_D3_1, Pcbgolf_2_2.SD_D3_1], name="SD_D3"),
        Net([STM_D_N_1, Pcbgolf_2_2.STM_D_N_1], name="STM_D_N"),
        Net([STM_D_P_1, Pcbgolf_2_2.STM_D_P_1], name="STM_D_P"),
    ]

    def __init__(self):
        self.place(self.Pcbgolf_2_1, Transform((0, 3.1191)))
        self.place(self.Pcbgolf_2_2, Transform((0, 8.8775)))
        self.place(self.Pcbgolf_2_3, Transform((42.6016, 0.984)))
        self.place(self.Pcbgolf_2_4, Transform((0, 35.386)))
        self.place(self.Pcbgolf_2_5, Transform((2.9968, 0)))
        self.place(self.Pcbgolf_2_6, Transform((11.9872, 2.844)))


from .components.UNKNOWN import DX07S024XJ1R1100 as DX07S024XJ1R1100
from .components.UNKNOWN import RC0402FR_0710KL as RC0402FR_0710KL
from .symbols.SymbolVBUS_2 import SymbolVBUS
class Pcbgolf_3_1(Circuit):
    GND_1 = Port()
    USB_D_N_1 = Port()
    USB_D_P_1 = Port()
    VBUS_1 = Port()

    J3 = DX07S024XJ1R1100.Device()
    R31 = RC0402FR_0710KL.Device()
    R32 = RC0402FR_0710KL.Device()
    R44 = RC0402FR_0710KL.Device()
    R45 = RC0402FR_0710KL.Device()

    nets = [
        Net([J3.CC1, R31.p[1], R32.p[1]], name="Net_J3_CC1"),
        Net([J3.CC2, R44.p[1], R45.p[1]], name="Net_J3_CC2_PadB5"),
        Net([GND_1, J3.GND[0], J3.GND[1], J3.GND[2], J3.GND[3], J3.SHIELDA, J3.SHIELDB, R31.p[2], R32.p[2], R44.p[2], R45.p[2]], name="GND"),
        Net([USB_D_N_1, J3.D_A, J3.D_B], name="USB_D_N"),
        Net([USB_D_P_1, J3.DA, J3.DB], name="USB_D_P"),
        Net([VBUS_1, J3.VBUS[0], J3.VBUS[1], J3.VBUS[2], J3.VBUS[3]], name="VBUS", symbol=SymbolVBUS()),
    ]

    def __init__(self):
        self.place(self.J3, Transform((42.0744, 0)))
        self.place(self.R31, Transform((0, 34.3265)))
        self.place(self.R32, Transform((0, 32.2995)))
        self.place(self.R44, Transform((2.9968, 38.3805)))
        self.place(self.R45, Transform((2.9968, 36.3535)))



from .components.UNKNOWN import GRM155R61A106ME11D as GRM155R61A106ME11D
from .components.UNKNOWN import Comp_47219_2001 as Comp_47219_2001
from .components.UNKNOWN import RC0402FR_0710KL as RC0402FR_0710KL
from .components.UNKNOWN import RMCF0402ZT0R00 as RMCF0402ZT0R00
from .symbols.SymbolU_3V3_2 import SymbolU_3V3
class Pcbgolf_3_2(Circuit):
    GND_1 = Port()
    SD_CLK_1 = Port()
    SD_CMD_1 = Port()
    SD_D0_1 = Port()
    SD_D1_1 = Port()
    SD_D2_1 = Port()
    SD_D3_1 = Port()
    U_3V3 = Port()

    C37 = GRM155R61A106ME11D.Device()
    J2 = Comp_47219_2001.Device()
    R33 = RC0402FR_0710KL.Device()
    R34 = RC0402FR_0710KL.Device()
    R35 = RC0402FR_0710KL.Device()
    R36 = RC0402FR_0710KL.Device()
    R37 = RC0402FR_0710KL.Device()
    R38 = RMCF0402ZT0R00.Device()
    R39 = RMCF0402ZT0R00.Device()
    R40 = RMCF0402ZT0R00.Device()
    R41 = RMCF0402ZT0R00.Device()
    R42 = RMCF0402ZT0R00.Device()
    R43 = RMCF0402ZT0R00.Device()

    nets = [
        Net([J2.CDDAT3, R36.p[2], R41.p[2]], name="Net_J2_CDslashDAT3"),
        Net([J2.CLK, R43.p[2]], name="Net_J2_CLK"),
        Net([J2.CMD, R37.p[2], R42.p[2]], name="Net_J2_CMD"),
        Net([J2.DAT0, R33.p[2], R38.p[2]], name="Net_J2_DAT0"),
        Net([J2.DAT1, R34.p[2], R39.p[2]], name="Net_J2_DAT1"),
        Net([J2.DAT2, R35.p[2], R40.p[2]], name="Net_J2_DAT2"),
        Net([GND_1, C37.p[2], J2.GND, J2.VSS], name="GND"),
        Net([U_3V3, C37.p[1], J2.VDD, R33.p[1], R34.p[1], R35.p[1], R36.p[1], R37.p[1]], name="Net3V3", symbol=SymbolU_3V3()),
        Net([SD_CLK_1, R43.p[1]], name="SD_CLK"),
        Net([SD_CMD_1, R42.p[1]], name="SD_CMD"),
        Net([SD_D0_1, R38.p[1]], name="SD_D0"),
        Net([SD_D1_1, R39.p[1]], name="SD_D1"),
        Net([SD_D2_1, R40.p[1]], name="SD_D2"),
        Net([SD_D3_1, R41.p[1]], name="SD_D3"),
    ]

    def __init__(self):
        self.place(self.C37, Transform((0, 4.054)))
        self.place(self.J2, Transform((61.5398, 16.878)))
        self.place(self.R33, Transform((8.9904, 4.054)))
        self.place(self.R34, Transform((8.9904, 2.027)))
        self.place(self.R35, Transform((8.9904, 0)))
        self.place(self.R36, Transform((11.9872, 28.378)))
        self.place(self.R37, Transform((11.9872, 26.351)))
        self.place(self.R38, Transform((11.9872, 24.324)))
        self.place(self.R39, Transform((11.9872, 22.297)))
        self.place(self.R40, Transform((11.9872, 20.27)))
        self.place(self.R41, Transform((11.9872, 18.243)))
        self.place(self.R42, Transform((11.9872, 16.216)))
        self.place(self.R43, Transform((11.9872, 14.189)))



from .components.UNKNOWN import CL05F104ZO5NNNC as CL05F104ZO5NNNC
from .symbols.SymbolU_3V3_2 import SymbolU_3V3
class Pcbgolf_3_3(Circuit):
    GND_1 = Port()
    U_3V3 = Port()

    C31 = CL05F104ZO5NNNC.Device()

    nets = [
        Net([GND_1, C31.p[1]], name="GND"),
        Net([U_3V3, C31.p[2]], name="Net3V3", symbol=SymbolU_3V3()),
    ]

    def __init__(self):
        self.place(self.C31, Transform((0, 0)))



from .components.UNKNOWN import C0402C120J5GACTU as C0402C120J5GACTU
from .components.UNKNOWN import GRM155R61A106ME11D as GRM155R61A106ME11D
from .components.UNKNOWN import CL05F104ZO5NNNC as CL05F104ZO5NNNC
from .components.UNKNOWN import RC0402JR_07100KL as RC0402JR_07100KL
from .components.UNKNOWN import RC0402JR_071ML as RC0402JR_071ML
from .components.UNKNOWN import CRGCQ0402F12K as CRGCQ0402F12K
from .components.UNKNOWN import RC0402FR_0710KL as RC0402FR_0710KL
from .components.UNKNOWN import USB2517 as USB2517
from .components.UNKNOWN import ABM8AIG_24_000MHZ_12_2Z_T3 as ABM8AIG_24_000MHZ_12_2Z_T3
from .symbols.SymbolVBUS_2 import SymbolVBUS
from .symbols.SymbolU_3V3_2 import SymbolU_3V3
class Pcbgolf_3_4(Circuit):
    CH1_D_N_1 = Port()
    CH1_D_P_1 = Port()
    CH2_D_N_1 = Port()
    CH2_D_P_1 = Port()
    CH3_D_N_1 = Port()
    CH3_D_P_1 = Port()
    CH4_D_N_1 = Port()
    CH4_D_P_1 = Port()
    GND_1 = Port()
    HUB_SCL_1 = Port()
    HUB_SDA_1 = Port()
    STM_D_N_1 = Port()
    STM_D_P_1 = Port()
    USB_D_N_1 = Port()
    USB_D_P_1 = Port()
    U_3V3 = Port()
    VBUS_1 = Port()

    C28 = C0402C120J5GACTU.Device()
    C29 = GRM155R61A106ME11D.Device()
    C32 = C0402C120J5GACTU.Device()
    C33 = GRM155R61A106ME11D.Device()
    C34 = GRM155R61A106ME11D.Device()
    C35 = CL05F104ZO5NNNC.Device()
    C36 = CL05F104ZO5NNNC.Device()
    R24 = RC0402JR_07100KL.Device()
    R25 = RC0402JR_07100KL.Device()
    R26 = RC0402JR_071ML.Device()
    R27 = CRGCQ0402F12K.Device()
    R28 = RC0402FR_0710KL.Device()
    R29 = RC0402FR_0710KL.Device()
    R30 = RC0402FR_0710KL.Device()
    U4 = USB2517.Device()
    Y2 = ABM8AIG_24_000MHZ_12_2Z_T3.Device()

    nets = [
        Net([R27.p[2], U4.RBIAS], name="Net_U4_RBIAS"),
        Net([R29.p[2], U4.SUSP_IND], name="Net_U4_SUSP_IND"),
        Net([R24.p[1], R25.p[2], U4.VBUS_DET], name="Net_U4_VBUS_DET"),
        Net([C33.p[1], C35.p[2], U4.VDD18], name="Net_U4_VDD18"),
        Net([C34.p[1], C36.p[2], U4.VDD18PLL], name="Net_U4_VDD18PLL"),
        Net([C28.p[1], R26.p[2], U4.XTAL1, Y2.p[1]], name="Net_U4_XTAL1"),
        Net([C32.p[1], R26.p[1], U4.XTAL2, Y2.p[2]], name="Net_U4_XTAL2"),
        Net([CH1_D_N_1, U4.USBDN1_DM], name="CH1_D_N"),
        Net([CH1_D_P_1, U4.USBDN1_DP], name="CH1_D_P"),
        Net([CH2_D_N_1, U4.USBDN2_DM], name="CH2_D_N"),
        Net([CH2_D_P_1, U4.USBDN2_DP], name="CH2_D_P"),
        Net([CH3_D_N_1, U4.USBDN3_DM], name="CH3_D_N"),
        Net([CH3_D_P_1, U4.USBDN3_DP], name="CH3_D_P"),
        Net([CH4_D_N_1, U4.USBDN4_DM], name="CH4_D_N"),
        Net([CH4_D_P_1, U4.USBDN4_DP], name="CH4_D_P"),
        Net([GND_1, C28.p[2], C29.p[2], C32.p[2], C33.p[2], C34.p[2], C35.p[1], C36.p[1], R25.p[1], R27.p[1], U4.TEST, U4.VSS, Y2.p[3]], name="GND"),
        Net([HUB_SCL_1, R30.p[2], U4.SCL], name="HUB_SCL"),
        Net([HUB_SDA_1, R28.p[2], U4.SDA], name="HUB_SDA"),
        Net([U_3V3, R28.p[1], R29.p[1], R30.p[1], U4.CFG_SEL1, U4.CFG_SEL2, U4.RESET_N, U4.VDD33, U4.VDD33CR, U4.VDD33PLL, U4.VDDA33], name="Net3V3", symbol=SymbolU_3V3()),
        Net([STM_D_N_1, U4.USBDN7_DM], name="STM_D_N"),
        Net([STM_D_P_1, U4.USBDN7_DP], name="STM_D_P"),
        Net([USB_D_N_1, U4.USBUP_DM], name="USB_D_N"),
        Net([USB_D_P_1, U4.USBUP_DP], name="USB_D_P"),
        Net([VBUS_1, C29.p[1], R24.p[2]], name="VBUS", symbol=SymbolVBUS()),
    ]

    def __init__(self):
        self.place(self.C28, Transform((0, 52.819)))
        self.place(self.C29, Transform((0, 50.792)))
        self.place(self.C32, Transform((0, 44.711)))
        self.place(self.C33, Transform((0, 42.684)))
        self.place(self.C34, Transform((0, 40.657)))
        self.place(self.C35, Transform((0, 38.63)))
        self.place(self.C36, Transform((0, 36.603)))
        self.place(self.R24, Transform((8.9904, 52.819)))
        self.place(self.R25, Transform((8.9904, 50.792)))
        self.place(self.R26, Transform((8.9904, 48.765)))
        self.place(self.R27, Transform((8.9904, 46.738)))
        self.place(self.R28, Transform((8.9904, 44.711)))
        self.place(self.R29, Transform((8.9904, 42.684)))
        self.place(self.R30, Transform((8.9904, 40.657)))
        self.place(self.U4, Transform((57.8948, 14.7185)))
        self.place(self.Y2, Transform((59.4283, 0)))



from .components.UNKNOWN import CL05F104ZO5NNNC as CL05F104ZO5NNNC
from .symbols.SymbolU_3V3_2 import SymbolU_3V3
class Pcbgolf_3_5(Circuit):
    GND_1 = Port()
    U_3V3 = Port()

    C30 = CL05F104ZO5NNNC.Device()

    nets = [
        Net([GND_1, C30.p[1]], name="GND"),
        Net([U_3V3, C30.p[2]], name="Net3V3", symbol=SymbolU_3V3()),
    ]

    def __init__(self):
        self.place(self.C30, Transform((0, 0)))



from .symbols.SymbolVBUS_2 import SymbolVBUS
from .symbols.SymbolU_3V3_2 import SymbolU_3V3
class Pcbgolf_3(Circuit):
    CH1_D_N_1 = Port()
    CH1_D_P_1 = Port()
    CH2_D_N_1 = Port()
    CH2_D_P_1 = Port()
    CH3_D_N_1 = Port()
    CH3_D_P_1 = Port()
    CH4_D_N_1 = Port()
    CH4_D_P_1 = Port()
    GND_1 = Port()
    HUB_SCL_1 = Port()
    HUB_SDA_1 = Port()
    SD_CLK_1 = Port()
    SD_CMD_1 = Port()
    SD_D0_1 = Port()
    SD_D1_1 = Port()
    SD_D2_1 = Port()
    SD_D3_1 = Port()
    STM_D_N_1 = Port()
    STM_D_P_1 = Port()
    U_3V3 = Port()

    Pcbgolf_3_1 = Pcbgolf_3_1()
    Pcbgolf_3_2 = Pcbgolf_3_2()
    Pcbgolf_3_3 = Pcbgolf_3_3()
    Pcbgolf_3_4 = Pcbgolf_3_4()
    Pcbgolf_3_5 = Pcbgolf_3_5()

    nets = [
        Net([Pcbgolf_3_1.USB_D_N_1, Pcbgolf_3_4.USB_D_N_1], name="USB_D_N"),
        Net([Pcbgolf_3_1.USB_D_P_1, Pcbgolf_3_4.USB_D_P_1], name="USB_D_P"),
        Net([Pcbgolf_3_1.VBUS_1, Pcbgolf_3_4.VBUS_1], name="VBUS", symbol=SymbolVBUS()),
        Net([CH1_D_N_1, Pcbgolf_3_4.CH1_D_N_1], name="CH1_D_N"),
        Net([CH1_D_P_1, Pcbgolf_3_4.CH1_D_P_1], name="CH1_D_P"),
        Net([CH2_D_N_1, Pcbgolf_3_4.CH2_D_N_1], name="CH2_D_N"),
        Net([CH2_D_P_1, Pcbgolf_3_4.CH2_D_P_1], name="CH2_D_P"),
        Net([CH3_D_N_1, Pcbgolf_3_4.CH3_D_N_1], name="CH3_D_N"),
        Net([CH3_D_P_1, Pcbgolf_3_4.CH3_D_P_1], name="CH3_D_P"),
        Net([CH4_D_N_1, Pcbgolf_3_4.CH4_D_N_1], name="CH4_D_N"),
        Net([CH4_D_P_1, Pcbgolf_3_4.CH4_D_P_1], name="CH4_D_P"),
        Net([GND_1, Pcbgolf_3_1.GND_1, Pcbgolf_3_2.GND_1, Pcbgolf_3_3.GND_1, Pcbgolf_3_4.GND_1, Pcbgolf_3_5.GND_1], name="GND"),
        Net([HUB_SCL_1, Pcbgolf_3_4.HUB_SCL_1], name="HUB_SCL"),
        Net([HUB_SDA_1, Pcbgolf_3_4.HUB_SDA_1], name="HUB_SDA"),
        Net([U_3V3, Pcbgolf_3_2.U_3V3, Pcbgolf_3_3.U_3V3, Pcbgolf_3_4.U_3V3, Pcbgolf_3_5.U_3V3], name="Net3V3", symbol=SymbolU_3V3()),
        Net([SD_CLK_1, Pcbgolf_3_2.SD_CLK_1], name="SD_CLK"),
        Net([SD_CMD_1, Pcbgolf_3_2.SD_CMD_1], name="SD_CMD"),
        Net([SD_D0_1, Pcbgolf_3_2.SD_D0_1], name="SD_D0"),
        Net([SD_D1_1, Pcbgolf_3_2.SD_D1_1], name="SD_D1"),
        Net([SD_D2_1, Pcbgolf_3_2.SD_D2_1], name="SD_D2"),
        Net([SD_D3_1, Pcbgolf_3_2.SD_D3_1], name="SD_D3"),
        Net([STM_D_N_1, Pcbgolf_3_4.STM_D_N_1], name="STM_D_N"),
        Net([STM_D_P_1, Pcbgolf_3_4.STM_D_P_1], name="STM_D_P"),
    ]

    def __init__(self):
        self.place(self.Pcbgolf_3_1, Transform((8.9904, 4.3035)))
        self.place(self.Pcbgolf_3_2, Transform((0, 30.522)))
        self.place(self.Pcbgolf_3_3, Transform((0, 46.738)))
        self.place(self.Pcbgolf_3_4, Transform((0, 0)))
        self.place(self.Pcbgolf_3_5, Transform((0, 48.765)))


from .symbols.SymbolU_5V_1 import SymbolU_5V
from .symbols.SymbolU_12V_2 import SymbolU_12V
from .symbols.SymbolU_3V3_2 import SymbolU_3V3
class Main(Circuit):
    CAN_FD = Pcbgolf_4()
    Channels = Pcbgolf_5()
    Power = Power()
    STM32H7 = Pcbgolf_2()
    USB__SD = Pcbgolf_3()

    nets = [
        Net([CAN_FD.CAN0_EN_1, STM32H7.CAN0_EN_1], name="CAN0_EN"),
        Net([CAN_FD.CAN0_H_1, Channels.CAN0_H_1], name="CAN0_H"),
        Net([CAN_FD.CAN0_L_1, Channels.CAN0_L_1], name="CAN0_L"),
        Net([CAN_FD.CAN0_RX_1, STM32H7.CAN0_RX_1], name="CAN0_RX"),
        Net([CAN_FD.CAN0_TX_1, STM32H7.CAN0_TX_1], name="CAN0_TX"),
        Net([CAN_FD.CAN1_EN_1, STM32H7.CAN1_EN_1], name="CAN1_EN"),
        Net([CAN_FD.CAN1_H_1, Channels.CAN1_H_1], name="CAN1_H"),
        Net([CAN_FD.CAN1_L_1, Channels.CAN1_L_1], name="CAN1_L"),
        Net([CAN_FD.CAN1_RX_1, STM32H7.CAN1_RX_1], name="CAN1_RX"),
        Net([CAN_FD.CAN1_TX_1, STM32H7.CAN1_TX_1], name="CAN1_TX"),
        Net([CAN_FD.CAN2_EN_1, STM32H7.CAN2_EN_1], name="CAN2_EN"),
        Net([CAN_FD.CAN2_H_1, Channels.CAN2_H_1], name="CAN2_H"),
        Net([CAN_FD.CAN2_L_1, Channels.CAN2_L_1], name="CAN2_L"),
        Net([CAN_FD.CAN2_RX_1, STM32H7.CAN2_RX_1], name="CAN2_RX"),
        Net([CAN_FD.CAN2_TX_1, STM32H7.CAN2_TX_1], name="CAN2_TX"),
        Net([CAN_FD.CAN3_EN_1, STM32H7.CAN3_EN_1], name="CAN3_EN"),
        Net([CAN_FD.CAN3_H_1, Channels.CAN3_H_1], name="CAN3_H"),
        Net([CAN_FD.CAN3_L_1, Channels.CAN3_L_1], name="CAN3_L"),
        Net([CAN_FD.CAN3_RX_1, STM32H7.CAN3_RX_1], name="CAN3_RX"),
        Net([CAN_FD.CAN3_TX_1, STM32H7.CAN3_TX_1], name="CAN3_TX"),
        Net([Channels.CH1_D_N_1, USB__SD.CH1_D_N_1], name="CH1_D_N"),
        Net([Channels.CH1_D_P_1, USB__SD.CH1_D_P_1], name="CH1_D_P"),
        Net([Channels.CH1_IMON_1, STM32H7.CH1_IMON_1], name="CH1_IMON"),
        Net([Channels.CH1_PWR_EN_1, STM32H7.CH1_PWR_EN_1], name="CH1_PWR_EN"),
        Net([Channels.CH1_SBU1_1, STM32H7.CH1_SBU1_1], name="CH1_SBU1"),
        Net([Channels.CH1_SBU1_IGN_1, STM32H7.CH1_SBU1_IGN_1], name="CH1_SBU1_IGN"),
        Net([Channels.CH1_SBU1_RELAY_1, STM32H7.CH1_SBU1_RELAY_1], name="CH1_SBU1_RELAY"),
        Net([Channels.CH1_SBU2_1, STM32H7.CH1_SBU2_1], name="CH1_SBU2"),
        Net([Channels.CH1_SBU2_IGN_1, STM32H7.CH1_SBU2_IGN_1], name="CH1_SBU2_IGN"),
        Net([Channels.CH1_SBU2_RELAY_1, STM32H7.CH1_SBU2_RELAY_1], name="CH1_SBU2_RELAY"),
        Net([Channels.CH2_D_N_1, USB__SD.CH2_D_N_1], name="CH2_D_N"),
        Net([Channels.CH2_D_P_1, USB__SD.CH2_D_P_1], name="CH2_D_P"),
        Net([Channels.CH2_IMON_1, STM32H7.CH2_IMON_1], name="CH2_IMON"),
        Net([Channels.CH2_PWR_EN_1, STM32H7.CH2_PWR_EN_1], name="CH2_PWR_EN"),
        Net([Channels.CH2_SBU1_1, STM32H7.CH2_SBU1_1], name="CH2_SBU1"),
        Net([Channels.CH2_SBU1_IGN_1, STM32H7.CH2_SBU1_IGN_1], name="CH2_SBU1_IGN"),
        Net([Channels.CH2_SBU1_RELAY_1, STM32H7.CH2_SBU1_RELAY_1], name="CH2_SBU1_RELAY"),
        Net([Channels.CH2_SBU2_1, STM32H7.CH2_SBU2_1], name="CH2_SBU2"),
        Net([Channels.CH2_SBU2_IGN_1, STM32H7.CH2_SBU2_IGN_1], name="CH2_SBU2_IGN"),
        Net([Channels.CH2_SBU2_RELAY_1, STM32H7.CH2_SBU2_RELAY_1], name="CH2_SBU2_RELAY"),
        Net([Channels.CH3_D_N_1, USB__SD.CH3_D_N_1], name="CH3_D_N"),
        Net([Channels.CH3_D_P_1, USB__SD.CH3_D_P_1], name="CH3_D_P"),
        Net([Channels.CH3_IMON_1, STM32H7.CH3_IMON_1], name="CH3_IMON"),
        Net([Channels.CH3_PWR_EN_1, STM32H7.CH3_PWR_EN_1], name="CH3_PWR_EN"),
        Net([Channels.CH3_SBU1_1, STM32H7.CH3_SBU1_1], name="CH3_SBU1"),
        Net([Channels.CH3_SBU1_IGN_1, STM32H7.CH3_SBU1_IGN_1], name="CH3_SBU1_IGN"),
        Net([Channels.CH3_SBU1_RELAY_1, STM32H7.CH3_SBU1_RELAY_1], name="CH3_SBU1_RELAY"),
        Net([Channels.CH3_SBU2_1, STM32H7.CH3_SBU2_1], name="CH3_SBU2"),
        Net([Channels.CH3_SBU2_IGN_1, STM32H7.CH3_SBU2_IGN_1], name="CH3_SBU2_IGN"),
        Net([Channels.CH3_SBU2_RELAY_1, STM32H7.CH3_SBU2_RELAY_1], name="CH3_SBU2_RELAY"),
        Net([Channels.CH4_D_N_1, USB__SD.CH4_D_N_1], name="CH4_D_N"),
        Net([Channels.CH4_D_P_1, USB__SD.CH4_D_P_1], name="CH4_D_P"),
        Net([Channels.CH4_IMON_1, STM32H7.CH4_IMON_1], name="CH4_IMON"),
        Net([Channels.CH4_PWR_EN_1, STM32H7.CH4_PWR_EN_1], name="CH4_PWR_EN"),
        Net([Channels.CH4_SBU1_1, STM32H7.CH4_SBU1_1], name="CH4_SBU1"),
        Net([Channels.CH4_SBU1_IGN_1, STM32H7.CH4_SBU1_IGN_1], name="CH4_SBU1_IGN"),
        Net([Channels.CH4_SBU1_RELAY_1, STM32H7.CH4_SBU1_RELAY_1], name="CH4_SBU1_RELAY"),
        Net([Channels.CH4_SBU2_1, STM32H7.CH4_SBU2_1], name="CH4_SBU2"),
        Net([Channels.CH4_SBU2_IGN_1, STM32H7.CH4_SBU2_IGN_1], name="CH4_SBU2_IGN"),
        Net([Channels.CH4_SBU2_RELAY_1, STM32H7.CH4_SBU2_RELAY_1], name="CH4_SBU2_RELAY"),
        Net([CAN_FD.GND_1, Channels.GND_1, Power.GND_1, STM32H7.GND_1, USB__SD.GND_1], name="GND"),
        Net([STM32H7.HUB_SCL_1, USB__SD.HUB_SCL_1], name="HUB_SCL"),
        Net([STM32H7.HUB_SDA_1, USB__SD.HUB_SDA_1], name="HUB_SDA"),
        Net([CAN_FD.U_12V, Channels.U_12V, Power.U_12V], name="Net12V", symbol=SymbolU_12V()),
        Net([CAN_FD.U_3V3, Power.U_3V3, STM32H7.U_3V3, USB__SD.U_3V3], name="Net3V3", symbol=SymbolU_3V3()),
        Net([CAN_FD.U_5V, Power.U_5V], name="Net5V", symbol=SymbolU_5V()),
        Net([STM32H7.SD_CLK_1, USB__SD.SD_CLK_1], name="SD_CLK"),
        Net([STM32H7.SD_CMD_1, USB__SD.SD_CMD_1], name="SD_CMD"),
        Net([STM32H7.SD_D0_1, USB__SD.SD_D0_1], name="SD_D0"),
        Net([STM32H7.SD_D1_1, USB__SD.SD_D1_1], name="SD_D1"),
        Net([STM32H7.SD_D2_1, USB__SD.SD_D2_1], name="SD_D2"),
        Net([STM32H7.SD_D3_1, USB__SD.SD_D3_1], name="SD_D3"),
        Net([STM32H7.STM_D_N_1, USB__SD.STM_D_N_1], name="STM_D_N"),
        Net([STM32H7.STM_D_P_1, USB__SD.STM_D_P_1], name="STM_D_P"),
    ]

    def __init__(self):
        self.place(self.CAN_FD, Transform((16.1654, 30.6281)))
        self.place(self.Channels, Transform((14.69102, 36.8226)))
        self.place(self.Power, Transform((13.1686, 29.4321)))
        self.place(self.STM32H7, Transform((13.1686, 30.0951)))
        self.place(self.USB__SD, Transform((16.1654, 34.9591)))

        self.Channels.Pcbgolf_5_03.J7.CC1.no_connect()
        self.Channels.Pcbgolf_5_03.J7.CC2.no_connect()
        self.Channels.Pcbgolf_5_03.U15.DMODE.no_connect()
        self.Channels.Pcbgolf_5_03.U15.DVDT.no_connect()
        self.Channels.Pcbgolf_5_03.U15.FLT_N.no_connect()
        self.Channels.Pcbgolf_5_03.U15.PG.no_connect()
        self.Channels.Pcbgolf_5_05.J8.CC1.no_connect()
        self.Channels.Pcbgolf_5_05.J8.CC2.no_connect()
        self.Channels.Pcbgolf_5_05.U16.DMODE.no_connect()
        self.Channels.Pcbgolf_5_05.U16.DVDT.no_connect()
        self.Channels.Pcbgolf_5_05.U16.FLT_N.no_connect()
        self.Channels.Pcbgolf_5_05.U16.PG.no_connect()
        self.Channels.Pcbgolf_5_07.J6.CC1.no_connect()
        self.Channels.Pcbgolf_5_07.J6.CC2.no_connect()
        self.Channels.Pcbgolf_5_07.U14.DMODE.no_connect()
        self.Channels.Pcbgolf_5_07.U14.DVDT.no_connect()
        self.Channels.Pcbgolf_5_07.U14.FLT_N.no_connect()
        self.Channels.Pcbgolf_5_07.U14.PG.no_connect()
        self.Channels.Pcbgolf_5_08.J5.CC1.no_connect()
        self.Channels.Pcbgolf_5_08.J5.CC2.no_connect()
        self.Channels.Pcbgolf_5_08.U13.DMODE.no_connect()
        self.Channels.Pcbgolf_5_08.U13.DVDT.no_connect()
        self.Channels.Pcbgolf_5_08.U13.FLT_N.no_connect()
        self.Channels.Pcbgolf_5_08.U13.PG.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.NRST.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PA10.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PA13JTMS.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PA14JTCK.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PA15JTDI.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PA2.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PA3.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PA7.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PA8.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PA9.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PB0.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PB14.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PB15.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PB2.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PC13.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PC14.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PC15.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PC5.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PC6.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PC7.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PE10.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PE11.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PE12.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PE13.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PE14.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PE5.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PE6.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PE7.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PE8.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PE9.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PF14.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PF15.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PF6.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PG11.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PG12.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PG13.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PG14.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PG6.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PG7.no_connect()
        self.STM32H7.Pcbgolf_2_2.U3.PG8.no_connect()
        self.USB__SD.Pcbgolf_3_1.J3.RX1n.no_connect()
        self.USB__SD.Pcbgolf_3_1.J3.RX1p.no_connect()
        self.USB__SD.Pcbgolf_3_1.J3.RX2n.no_connect()
        self.USB__SD.Pcbgolf_3_1.J3.RX2p.no_connect()
        self.USB__SD.Pcbgolf_3_1.J3.SBU1.no_connect()
        self.USB__SD.Pcbgolf_3_1.J3.SBU2.no_connect()
        self.USB__SD.Pcbgolf_3_1.J3.TX1n.no_connect()
        self.USB__SD.Pcbgolf_3_1.J3.TX1p.no_connect()
        self.USB__SD.Pcbgolf_3_1.J3.TX2n.no_connect()
        self.USB__SD.Pcbgolf_3_1.J3.TX2p.no_connect()
        self.USB__SD.Pcbgolf_3_4.U4.LED_A1_N.no_connect()
        self.USB__SD.Pcbgolf_3_4.U4.LED_A2_N.no_connect()
        self.USB__SD.Pcbgolf_3_4.U4.LED_A3_N.no_connect()
        self.USB__SD.Pcbgolf_3_4.U4.LED_A4_N.no_connect()
        self.USB__SD.Pcbgolf_3_4.U4.LED_A5_N.no_connect()
        self.USB__SD.Pcbgolf_3_4.U4.LED_A6_N.no_connect()
        self.USB__SD.Pcbgolf_3_4.U4.LED_A7_N.no_connect()
        self.USB__SD.Pcbgolf_3_4.U4.LED_B1_N.no_connect()
        self.USB__SD.Pcbgolf_3_4.U4.LED_B2_N.no_connect()
        self.USB__SD.Pcbgolf_3_4.U4.LED_B3_N.no_connect()
        self.USB__SD.Pcbgolf_3_4.U4.LED_B4_N.no_connect()
        self.USB__SD.Pcbgolf_3_4.U4.LED_B5_N.no_connect()
        self.USB__SD.Pcbgolf_3_4.U4.LED_B6_N.no_connect()
        self.USB__SD.Pcbgolf_3_4.U4.LED_B7_N.no_connect()
        self.USB__SD.Pcbgolf_3_4.U4.OCS1_N.no_connect()
        self.USB__SD.Pcbgolf_3_4.U4.OCS2_N.no_connect()
        self.USB__SD.Pcbgolf_3_4.U4.OCS3_N.no_connect()
        self.USB__SD.Pcbgolf_3_4.U4.OCS4_N.no_connect()
        self.USB__SD.Pcbgolf_3_4.U4.OCS5_N.no_connect()
        self.USB__SD.Pcbgolf_3_4.U4.OCS6_N.no_connect()
        self.USB__SD.Pcbgolf_3_4.U4.OCS7_N.no_connect()
        self.USB__SD.Pcbgolf_3_4.U4.PRTPWR1.no_connect()
        self.USB__SD.Pcbgolf_3_4.U4.PRTPWR2.no_connect()
        self.USB__SD.Pcbgolf_3_4.U4.PRTPWR3.no_connect()
        self.USB__SD.Pcbgolf_3_4.U4.PRTPWR4.no_connect()
        self.USB__SD.Pcbgolf_3_4.U4.PRTPWR5.no_connect()
        self.USB__SD.Pcbgolf_3_4.U4.PRTPWR6.no_connect()
        self.USB__SD.Pcbgolf_3_4.U4.PRTPWR7.no_connect()
        self.USB__SD.Pcbgolf_3_4.U4.USBDN5_DM.no_connect()
        self.USB__SD.Pcbgolf_3_4.U4.USBDN5_DP.no_connect()
        self.USB__SD.Pcbgolf_3_4.U4.USBDN6_DM.no_connect()
        self.USB__SD.Pcbgolf_3_4.U4.USBDN6_DP.no_connect()

        self.CAN_FD.Pcbgolf_4_01.LED5.reference_designator = "LED5"
        self.CAN_FD.Pcbgolf_4_01.R59.reference_designator = "R59"
        self.CAN_FD.Pcbgolf_4_01.R60.reference_designator = "R60"
        self.CAN_FD.Pcbgolf_4_01.R61.reference_designator = "R61"
        self.CAN_FD.Pcbgolf_4_01.R65.reference_designator = "R65"
        self.CAN_FD.Pcbgolf_4_01.U12.reference_designator = "U12"
        self.CAN_FD.Pcbgolf_4_02.LED4.reference_designator = "LED4"
        self.CAN_FD.Pcbgolf_4_02.R56.reference_designator = "R56"
        self.CAN_FD.Pcbgolf_4_02.R57.reference_designator = "R57"
        self.CAN_FD.Pcbgolf_4_02.R58.reference_designator = "R58"
        self.CAN_FD.Pcbgolf_4_02.R64.reference_designator = "R64"
        self.CAN_FD.Pcbgolf_4_02.U11.reference_designator = "U11"
        self.CAN_FD.Pcbgolf_4_03.LED3.reference_designator = "LED3"
        self.CAN_FD.Pcbgolf_4_03.R53.reference_designator = "R53"
        self.CAN_FD.Pcbgolf_4_03.R54.reference_designator = "R54"
        self.CAN_FD.Pcbgolf_4_03.R55.reference_designator = "R55"
        self.CAN_FD.Pcbgolf_4_03.R63.reference_designator = "R63"
        self.CAN_FD.Pcbgolf_4_03.U10.reference_designator = "U10"
        self.CAN_FD.Pcbgolf_4_04.C49.reference_designator = "C49"
        self.CAN_FD.Pcbgolf_4_05.C48.reference_designator = "C48"
        self.CAN_FD.Pcbgolf_4_06.C47.reference_designator = "C47"
        self.CAN_FD.Pcbgolf_4_07.C46.reference_designator = "C46"
        self.CAN_FD.Pcbgolf_4_08.C45.reference_designator = "C45"
        self.CAN_FD.Pcbgolf_4_09.C44.reference_designator = "C44"
        self.CAN_FD.Pcbgolf_4_10.C43.reference_designator = "C43"
        self.CAN_FD.Pcbgolf_4_11.C42.reference_designator = "C42"
        self.CAN_FD.Pcbgolf_4_12.C41.reference_designator = "C41"
        self.CAN_FD.Pcbgolf_4_13.C40.reference_designator = "C40"
        self.CAN_FD.Pcbgolf_4_14.C39.reference_designator = "C39"
        self.CAN_FD.Pcbgolf_4_15.C38.reference_designator = "C38"
        self.CAN_FD.Pcbgolf_4_16.J4.reference_designator = "J4"
        self.CAN_FD.Pcbgolf_4_17.L8.reference_designator = "L8"
        self.CAN_FD.Pcbgolf_4_17.U8.reference_designator = "U8"
        self.CAN_FD.Pcbgolf_4_18.L7.reference_designator = "L7"
        self.CAN_FD.Pcbgolf_4_18.U7.reference_designator = "U7"
        self.CAN_FD.Pcbgolf_4_19.L6.reference_designator = "L6"
        self.CAN_FD.Pcbgolf_4_19.U6.reference_designator = "U6"
        self.CAN_FD.Pcbgolf_4_20.L5.reference_designator = "L5"
        self.CAN_FD.Pcbgolf_4_20.U5.reference_designator = "U5"
        self.CAN_FD.Pcbgolf_4_21.LED2.reference_designator = "LED2"
        self.CAN_FD.Pcbgolf_4_21.R50.reference_designator = "R50"
        self.CAN_FD.Pcbgolf_4_21.R51.reference_designator = "R51"
        self.CAN_FD.Pcbgolf_4_21.R52.reference_designator = "R52"
        self.CAN_FD.Pcbgolf_4_21.R62.reference_designator = "R62"
        self.CAN_FD.Pcbgolf_4_21.U9.reference_designator = "U9"
        self.CAN_FD.Pcbgolf_4_22.R49.reference_designator = "R49"
        self.CAN_FD.Pcbgolf_4_23.R48.reference_designator = "R48"
        self.CAN_FD.Pcbgolf_4_24.R47.reference_designator = "R47"
        self.CAN_FD.Pcbgolf_4_25.R46.reference_designator = "R46"
        self.Channels.Pcbgolf_5_01.Q4.reference_designator = "Q4"
        self.Channels.Pcbgolf_5_01.R100.reference_designator = "R100"
        self.Channels.Pcbgolf_5_01.R80.reference_designator = "R80"
        self.Channels.Pcbgolf_5_01.R94.reference_designator = "R94"
        self.Channels.Pcbgolf_5_01.R95.reference_designator = "R95"
        self.Channels.Pcbgolf_5_02.Q3.reference_designator = "Q3"
        self.Channels.Pcbgolf_5_02.R79.reference_designator = "R79"
        self.Channels.Pcbgolf_5_02.R92.reference_designator = "R92"
        self.Channels.Pcbgolf_5_02.R93.reference_designator = "R93"
        self.Channels.Pcbgolf_5_02.R99.reference_designator = "R99"
        self.Channels.Pcbgolf_5_03.C52.reference_designator = "C52"
        self.Channels.Pcbgolf_5_03.J7.reference_designator = "J7"
        self.Channels.Pcbgolf_5_03.LED8.reference_designator = "LED8"
        self.Channels.Pcbgolf_5_03.R68.reference_designator = "R68"
        self.Channels.Pcbgolf_5_03.R72.reference_designator = "R72"
        self.Channels.Pcbgolf_5_03.R76.reference_designator = "R76"
        self.Channels.Pcbgolf_5_03.U15.reference_designator = "U15"
        self.Channels.Pcbgolf_5_04.Q8.reference_designator = "Q8"
        self.Channels.Pcbgolf_5_04.R104.reference_designator = "R104"
        self.Channels.Pcbgolf_5_04.R118.reference_designator = "R118"
        self.Channels.Pcbgolf_5_04.R119.reference_designator = "R119"
        self.Channels.Pcbgolf_5_04.R124.reference_designator = "R124"
        self.Channels.Pcbgolf_5_05.C53.reference_designator = "C53"
        self.Channels.Pcbgolf_5_05.J8.reference_designator = "J8"
        self.Channels.Pcbgolf_5_05.LED9.reference_designator = "LED9"
        self.Channels.Pcbgolf_5_05.R69.reference_designator = "R69"
        self.Channels.Pcbgolf_5_05.R73.reference_designator = "R73"
        self.Channels.Pcbgolf_5_05.R77.reference_designator = "R77"
        self.Channels.Pcbgolf_5_05.U16.reference_designator = "U16"
        self.Channels.Pcbgolf_5_06.Q6.reference_designator = "Q6"
        self.Channels.Pcbgolf_5_06.R102.reference_designator = "R102"
        self.Channels.Pcbgolf_5_06.R114.reference_designator = "R114"
        self.Channels.Pcbgolf_5_06.R115.reference_designator = "R115"
        self.Channels.Pcbgolf_5_06.R122.reference_designator = "R122"
        self.Channels.Pcbgolf_5_07.C51.reference_designator = "C51"
        self.Channels.Pcbgolf_5_07.J6.reference_designator = "J6"
        self.Channels.Pcbgolf_5_07.LED7.reference_designator = "LED7"
        self.Channels.Pcbgolf_5_07.R67.reference_designator = "R67"
        self.Channels.Pcbgolf_5_07.R71.reference_designator = "R71"
        self.Channels.Pcbgolf_5_07.R75.reference_designator = "R75"
        self.Channels.Pcbgolf_5_07.U14.reference_designator = "U14"
        self.Channels.Pcbgolf_5_08.C50.reference_designator = "C50"
        self.Channels.Pcbgolf_5_08.J5.reference_designator = "J5"
        self.Channels.Pcbgolf_5_08.LED6.reference_designator = "LED6"
        self.Channels.Pcbgolf_5_08.R66.reference_designator = "R66"
        self.Channels.Pcbgolf_5_08.R70.reference_designator = "R70"
        self.Channels.Pcbgolf_5_08.R74.reference_designator = "R74"
        self.Channels.Pcbgolf_5_08.U13.reference_designator = "U13"
        self.Channels.Pcbgolf_5_09.LED11.reference_designator = "LED11"
        self.Channels.Pcbgolf_5_09.R84.reference_designator = "R84"
        self.Channels.Pcbgolf_5_09.R85.reference_designator = "R85"
        self.Channels.Pcbgolf_5_10.Q7.reference_designator = "Q7"
        self.Channels.Pcbgolf_5_10.R103.reference_designator = "R103"
        self.Channels.Pcbgolf_5_10.R116.reference_designator = "R116"
        self.Channels.Pcbgolf_5_10.R117.reference_designator = "R117"
        self.Channels.Pcbgolf_5_10.R123.reference_designator = "R123"
        self.Channels.Pcbgolf_5_11.Q5.reference_designator = "Q5"
        self.Channels.Pcbgolf_5_11.R101.reference_designator = "R101"
        self.Channels.Pcbgolf_5_11.R81.reference_designator = "R81"
        self.Channels.Pcbgolf_5_11.R96.reference_designator = "R96"
        self.Channels.Pcbgolf_5_11.R97.reference_designator = "R97"
        self.Channels.Pcbgolf_5_12.Q2.reference_designator = "Q2"
        self.Channels.Pcbgolf_5_12.R78.reference_designator = "R78"
        self.Channels.Pcbgolf_5_12.R90.reference_designator = "R90"
        self.Channels.Pcbgolf_5_12.R91.reference_designator = "R91"
        self.Channels.Pcbgolf_5_12.R98.reference_designator = "R98"
        self.Channels.Pcbgolf_5_13.LED17.reference_designator = "LED17"
        self.Channels.Pcbgolf_5_13.R112.reference_designator = "R112"
        self.Channels.Pcbgolf_5_13.R113.reference_designator = "R113"
        self.Channels.Pcbgolf_5_14.LED16.reference_designator = "LED16"
        self.Channels.Pcbgolf_5_14.R110.reference_designator = "R110"
        self.Channels.Pcbgolf_5_14.R111.reference_designator = "R111"
        self.Channels.Pcbgolf_5_15.LED15.reference_designator = "LED15"
        self.Channels.Pcbgolf_5_15.R108.reference_designator = "R108"
        self.Channels.Pcbgolf_5_15.R109.reference_designator = "R109"
        self.Channels.Pcbgolf_5_16.LED14.reference_designator = "LED14"
        self.Channels.Pcbgolf_5_16.R106.reference_designator = "R106"
        self.Channels.Pcbgolf_5_16.R107.reference_designator = "R107"
        self.Channels.Pcbgolf_5_17.LED13.reference_designator = "LED13"
        self.Channels.Pcbgolf_5_17.R88.reference_designator = "R88"
        self.Channels.Pcbgolf_5_17.R89.reference_designator = "R89"
        self.Channels.Pcbgolf_5_18.LED12.reference_designator = "LED12"
        self.Channels.Pcbgolf_5_18.R86.reference_designator = "R86"
        self.Channels.Pcbgolf_5_18.R87.reference_designator = "R87"
        self.Channels.Pcbgolf_5_19.LED10.reference_designator = "LED10"
        self.Channels.Pcbgolf_5_19.R82.reference_designator = "R82"
        self.Channels.Pcbgolf_5_19.R83.reference_designator = "R83"
        self.Channels.Pcbgolf_5_20.Q9.reference_designator = "Q9"
        self.Channels.Pcbgolf_5_20.R105.reference_designator = "R105"
        self.Channels.Pcbgolf_5_20.R120.reference_designator = "R120"
        self.Channels.Pcbgolf_5_20.R121.reference_designator = "R121"
        self.Channels.Pcbgolf_5_20.R125.reference_designator = "R125"
        self.Power.Power_1.C1.reference_designator = "C1"
        self.Power.Power_1.C2.reference_designator = "C2"
        self.Power.Power_1.C4.reference_designator = "C4"
        self.Power.Power_1.C6.reference_designator = "C6"
        self.Power.Power_1.C7.reference_designator = "C7"
        self.Power.Power_1.C8.reference_designator = "C8"
        self.Power.Power_1.L1.reference_designator = "L1"
        self.Power.Power_1.R1.reference_designator = "R1"
        self.Power.Power_1.R3.reference_designator = "R3"
        self.Power.Power_1.R4.reference_designator = "R4"
        self.Power.Power_1.R5.reference_designator = "R5"
        self.Power.Power_1.R6.reference_designator = "R6"
        self.Power.Power_1.U1.reference_designator = "U1"
        self.Power.Power_2.C10.reference_designator = "C10"
        self.Power.Power_2.C11.reference_designator = "C11"
        self.Power.Power_2.C12.reference_designator = "C12"
        self.Power.Power_2.C13.reference_designator = "C13"
        self.Power.Power_2.C3.reference_designator = "C3"
        self.Power.Power_2.C5.reference_designator = "C5"
        self.Power.Power_2.C9.reference_designator = "C9"
        self.Power.Power_2.D1.reference_designator = "D1"
        self.Power.Power_2.D2.reference_designator = "D2"
        self.Power.Power_2.J1.reference_designator = "J1"
        self.Power.Power_2.L2.reference_designator = "L2"
        self.Power.Power_2.Q1.reference_designator = "Q1"
        self.Power.Power_2.R10.reference_designator = "R10"
        self.Power.Power_2.R2.reference_designator = "R2"
        self.Power.Power_2.R7.reference_designator = "R7"
        self.Power.Power_2.R8.reference_designator = "R8"
        self.Power.Power_2.R9.reference_designator = "R9"
        self.Power.Power_2.U2.reference_designator = "U2"
        self.Power.Power_3.BH4.reference_designator = "BH4"
        self.Power.Power_4.BH3.reference_designator = "BH3"
        self.Power.Power_5.BH2.reference_designator = "BH2"
        self.Power.Power_6.BH1.reference_designator = "BH1"
        self.STM32H7.Pcbgolf_2_1.C22.reference_designator = "C22"
        self.STM32H7.Pcbgolf_2_1.L3.reference_designator = "L3"
        self.STM32H7.Pcbgolf_2_2.C14.reference_designator = "C14"
        self.STM32H7.Pcbgolf_2_2.C15.reference_designator = "C15"
        self.STM32H7.Pcbgolf_2_2.C16.reference_designator = "C16"
        self.STM32H7.Pcbgolf_2_2.C17.reference_designator = "C17"
        self.STM32H7.Pcbgolf_2_2.C18.reference_designator = "C18"
        self.STM32H7.Pcbgolf_2_2.R11.reference_designator = "R11"
        self.STM32H7.Pcbgolf_2_2.R12.reference_designator = "R12"
        self.STM32H7.Pcbgolf_2_2.R13.reference_designator = "R13"
        self.STM32H7.Pcbgolf_2_2.R14.reference_designator = "R14"
        self.STM32H7.Pcbgolf_2_2.R15.reference_designator = "R15"
        self.STM32H7.Pcbgolf_2_2.R16.reference_designator = "R16"
        self.STM32H7.Pcbgolf_2_2.R17.reference_designator = "R17"
        self.STM32H7.Pcbgolf_2_2.R18.reference_designator = "R18"
        self.STM32H7.Pcbgolf_2_2.R19.reference_designator = "R19"
        self.STM32H7.Pcbgolf_2_2.R20.reference_designator = "R20"
        self.STM32H7.Pcbgolf_2_2.U3.reference_designator = "U3"
        self.STM32H7.Pcbgolf_2_2.Y1.reference_designator = "Y1"
        self.STM32H7.Pcbgolf_2_3.SW1.reference_designator = "SW1"
        self.STM32H7.Pcbgolf_2_4.C19.reference_designator = "C19"
        self.STM32H7.Pcbgolf_2_4.C20.reference_designator = "C20"
        self.STM32H7.Pcbgolf_2_4.C23.reference_designator = "C23"
        self.STM32H7.Pcbgolf_2_4.C24.reference_designator = "C24"
        self.STM32H7.Pcbgolf_2_4.C26.reference_designator = "C26"
        self.STM32H7.Pcbgolf_2_4.C27.reference_designator = "C27"
        self.STM32H7.Pcbgolf_2_5.C21.reference_designator = "C21"
        self.STM32H7.Pcbgolf_2_5.C25.reference_designator = "C25"
        self.STM32H7.Pcbgolf_2_5.L4.reference_designator = "L4"
        self.STM32H7.Pcbgolf_2_6.LED1.reference_designator = "LED1"
        self.STM32H7.Pcbgolf_2_6.R21.reference_designator = "R21"
        self.STM32H7.Pcbgolf_2_6.R22.reference_designator = "R22"
        self.STM32H7.Pcbgolf_2_6.R23.reference_designator = "R23"
        self.USB__SD.Pcbgolf_3_1.J3.reference_designator = "J3"
        self.USB__SD.Pcbgolf_3_1.R31.reference_designator = "R31"
        self.USB__SD.Pcbgolf_3_1.R32.reference_designator = "R32"
        self.USB__SD.Pcbgolf_3_1.R44.reference_designator = "R44"
        self.USB__SD.Pcbgolf_3_1.R45.reference_designator = "R45"
        self.USB__SD.Pcbgolf_3_2.C37.reference_designator = "C37"
        self.USB__SD.Pcbgolf_3_2.J2.reference_designator = "J2"
        self.USB__SD.Pcbgolf_3_2.R33.reference_designator = "R33"
        self.USB__SD.Pcbgolf_3_2.R34.reference_designator = "R34"
        self.USB__SD.Pcbgolf_3_2.R35.reference_designator = "R35"
        self.USB__SD.Pcbgolf_3_2.R36.reference_designator = "R36"
        self.USB__SD.Pcbgolf_3_2.R37.reference_designator = "R37"
        self.USB__SD.Pcbgolf_3_2.R38.reference_designator = "R38"
        self.USB__SD.Pcbgolf_3_2.R39.reference_designator = "R39"
        self.USB__SD.Pcbgolf_3_2.R40.reference_designator = "R40"
        self.USB__SD.Pcbgolf_3_2.R41.reference_designator = "R41"
        self.USB__SD.Pcbgolf_3_2.R42.reference_designator = "R42"
        self.USB__SD.Pcbgolf_3_2.R43.reference_designator = "R43"
        self.USB__SD.Pcbgolf_3_3.C31.reference_designator = "C31"
        self.USB__SD.Pcbgolf_3_4.C28.reference_designator = "C28"
        self.USB__SD.Pcbgolf_3_4.C29.reference_designator = "C29"
        self.USB__SD.Pcbgolf_3_4.C32.reference_designator = "C32"
        self.USB__SD.Pcbgolf_3_4.C33.reference_designator = "C33"
        self.USB__SD.Pcbgolf_3_4.C34.reference_designator = "C34"
        self.USB__SD.Pcbgolf_3_4.C35.reference_designator = "C35"
        self.USB__SD.Pcbgolf_3_4.C36.reference_designator = "C36"
        self.USB__SD.Pcbgolf_3_4.R24.reference_designator = "R24"
        self.USB__SD.Pcbgolf_3_4.R25.reference_designator = "R25"
        self.USB__SD.Pcbgolf_3_4.R26.reference_designator = "R26"
        self.USB__SD.Pcbgolf_3_4.R27.reference_designator = "R27"
        self.USB__SD.Pcbgolf_3_4.R28.reference_designator = "R28"
        self.USB__SD.Pcbgolf_3_4.R29.reference_designator = "R29"
        self.USB__SD.Pcbgolf_3_4.R30.reference_designator = "R30"
        self.USB__SD.Pcbgolf_3_4.U4.reference_designator = "U4"
        self.USB__SD.Pcbgolf_3_4.Y2.reference_designator = "Y2"
        self.USB__SD.Pcbgolf_3_5.C30.reference_designator = "C30"



# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/components/UNKNOWN/RH100_25_000_12_F_1010_TR.py 
# To import this component:
#     from .components.UNKNOWN import RH100_25_000_12_F_1010_TR
#     u1 = RH100_25_000_12_F_1010_TR.RH100_25_000_12_F_1010_TR()
from jitx.component import Component
from jitx.net import Port
from jitx.landpattern import PadMapping
from jitx.symbol import SymbolMapping


from ...landpatterns.LandpatternXTAL_3_2X2_5 import LandpatternXTAL_3_2X2_5
from ...symbols.Symbolcomma_ai_11112255_CRYSTAL_4PIN4_PIN_1 import Symbolcomma_ai_11112255_CRYSTAL_4PIN4_PIN
class RH100_25_000_12_F_1010_TR(Component):
    description = ""
    mpn = "RH100-25.000-12-F-1010-TR"
    datasheet = ""
    reference_designator_prefix = "Y"
    landpattern = LandpatternXTAL_3_2X2_5()
    p = {
        1: Port(),
        2: Port(),
        3: Port(),
    }
    symbol = Symbolcomma_ai_11112255_CRYSTAL_4PIN4_PIN()
    mappings = [
        SymbolMapping({
            p[1]: symbol.p[1], 
            p[2]: symbol.p[2], 
            p[3]: symbol.p[3]
        }),
        PadMapping({
            p[1]: landpattern.p[1],
            p[2]: landpattern.p[3],
            p[3]: [
                landpattern.p[4],
                landpattern.p[2],
            ],
        }),
    ]

Device: type[RH100_25_000_12_F_1010_TR] = RH100_25_000_12_F_1010_TR

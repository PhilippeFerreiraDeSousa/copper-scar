# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/components/UNKNOWN/RC0402JR_07100RL.py 
# To import this component:
#     from .components.UNKNOWN import RC0402JR_07100RL
#     u1 = RC0402JR_07100RL.RC0402JR_07100RL()
from jitx.component import Component
from jitx.net import Port
from jitx.landpattern import PadMapping
from jitx.symbol import SymbolMapping


from ...landpatterns.LandpatternU0402_R import LandpatternU0402_R
from ...symbols.Symbolcomma_ai_11112255_R0402 import Symbolcomma_ai_11112255_R0402
class RC0402JR_07100RL(Component):
    description = ""
    mpn = "RC0402JR-07100RL"
    datasheet = ""
    reference_designator_prefix = "R"
    landpattern = LandpatternU0402_R()
    p = {
        1: Port(),
        2: Port(),
    }
    symbol = Symbolcomma_ai_11112255_R0402()
    mappings = [
        SymbolMapping({
            p[1]: symbol.p[1], 
            p[2]: symbol.p[2]
        }),
        PadMapping({
            p[1]: landpattern.p[1],
            p[2]: landpattern.p[2],
        }),
    ]

Device: type[RC0402JR_07100RL] = RC0402JR_07100RL

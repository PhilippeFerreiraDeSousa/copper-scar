# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/components/UNKNOWN/CRGCQ0402F12K.py 
# To import this component:
#     from .components.UNKNOWN import CRGCQ0402F12K
#     u1 = CRGCQ0402F12K.CRGCQ0402F12K()
from jitx.component import Component
from jitx.net import Port
from jitx.landpattern import PadMapping
from jitx.symbol import SymbolMapping


from ...landpatterns.LandpatternU0402_R import LandpatternU0402_R
from ...symbols.Symbolcomma_ai_11112255_R0402 import Symbolcomma_ai_11112255_R0402
class CRGCQ0402F12K(Component):
    description = ""
    mpn = "CRGCQ0402F12K"
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

Device: type[CRGCQ0402F12K] = CRGCQ0402F12K

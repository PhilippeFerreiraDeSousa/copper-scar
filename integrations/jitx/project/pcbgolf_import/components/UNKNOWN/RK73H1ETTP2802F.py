# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/components/UNKNOWN/RK73H1ETTP2802F.py 
# To import this component:
#     from .components.UNKNOWN import RK73H1ETTP2802F
#     u1 = RK73H1ETTP2802F.RK73H1ETTP2802F()
from jitx.component import Component
from jitx.net import Port
from jitx.landpattern import PadMapping
from jitx.symbol import SymbolMapping


from ...landpatterns.LandpatternU0402_R import LandpatternU0402_R
from ...symbols.Symbolcomma_ai_11112255_R0402 import Symbolcomma_ai_11112255_R0402
class RK73H1ETTP2802F(Component):
    description = ""
    mpn = "RK73H1ETTP2802F"
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

Device: type[RK73H1ETTP2802F] = RK73H1ETTP2802F

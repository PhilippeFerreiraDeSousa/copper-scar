# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/components/UNKNOWN/C0402C120J5GACTU.py 
# To import this component:
#     from .components.UNKNOWN import C0402C120J5GACTU
#     u1 = C0402C120J5GACTU.C0402C120J5GACTU()
from jitx.component import Component
from jitx.net import Port
from jitx.landpattern import PadMapping
from jitx.symbol import SymbolMapping


from ...landpatterns.LandpatternU0402_C import LandpatternU0402_C
from ...symbols.Symbolcomma_ai_11112255_C0402_1 import Symbolcomma_ai_11112255_C0402
class C0402C120J5GACTU(Component):
    description = ""
    mpn = "C0402C120J5GACTU"
    datasheet = ""
    reference_designator_prefix = "C"
    landpattern = LandpatternU0402_C()
    p = {
        1: Port(),
        2: Port(),
    }
    symbol = Symbolcomma_ai_11112255_C0402()
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

Device: type[C0402C120J5GACTU] = C0402C120J5GACTU

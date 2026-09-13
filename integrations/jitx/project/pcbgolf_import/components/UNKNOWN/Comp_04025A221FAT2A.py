# File Location: b-unassigned-nc-output/converted/imports/Pcbgolf/components/UNKNOWN/Comp_04025A221FAT2A.py 
# To import this component:
#     from .components.UNKNOWN import Comp_04025A221FAT2A
#     u1 = Comp_04025A221FAT2A.Comp_04025A221FAT2A()
from jitx.component import Component
from jitx.net import Port
from jitx.landpattern import PadMapping
from jitx.symbol import SymbolMapping


from ...landpatterns.LandpatternU0402_C import LandpatternU0402_C
from ...symbols.Symbolcomma_ai_11112255_C0402_1 import Symbolcomma_ai_11112255_C0402
class Comp_04025A221FAT2A(Component):
    description = ""
    mpn = "04025A221FAT2A"
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

Device: type[Comp_04025A221FAT2A] = Comp_04025A221FAT2A

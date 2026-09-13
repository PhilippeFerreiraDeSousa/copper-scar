"""Represent physical pads with distinct ports on the same electrical net.

Uses public Component, PadMapping, Port and Net fields. Apply during construction
of a NEW diagnostic parent; never silently alter an accepted existing parent.
"""
from jitx.landpattern import PadMapping
from jitx.net import Port, Net
from jitx.symbol import Symbol, Pin, Direction, SymbolMapping

class AdditionalPadPins(Symbol):
    def __init__(self,count):
        self.pins={str(i):Pin((0,2*i),1,Direction.Right) for i in range(count)}

def split_pad_ports(component):
    ports={};ties=[];mappings=[]
    for mapping in component.mappings:
        if not isinstance(mapping,PadMapping):
            mappings.append(mapping);continue
        entries={}
        for port,pads in mapping.items():
            if not isinstance(pads,(list,tuple)):
                entries[port]=pads;continue
            entries[port]=pads[0]
            for pad in pads[1:]:
                extra=Port();ports['pad_'+str(len(ports))]=extra
                entries[extra]=pad;ties.append(Net([port,extra]))
        mappings.append(PadMapping(entries))
    component.split_pad_ports=ports
    component.additional_pad_symbol=AdditionalPadPins(len(ports))
    mappings.append(SymbolMapping({port:component.additional_pad_symbol.pins[str(i)] for i,port in enumerate(ports.values())}))
    component.mappings=mappings
    return ties

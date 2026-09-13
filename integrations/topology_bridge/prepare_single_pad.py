"""Minimal single-pad public-API reproducer, isolated source only."""
import json
from pathlib import Path
import subprocess
import sys
root=Path(sys.argv[1]).absolute();pad=sys.argv[2]
subprocess.run([sys.executable,str(Path(__file__).with_name('prepare_capture_reduction.py')),str(root),'J3'],check=True)
source=f'''from jitx.board import Board
from jitx.circuit import Circuit
from jitx.component import Component
from jitx.design import Design
from jitx.landpattern import Landpattern, PadMapping
from jitx.net import Port
from jitx.shapes.composites import rectangle
from jitx.symbol import Symbol, Pin, Direction, SymbolMapping
from proxy_import.board import SubstratePcbgolf
from proxy_import.components.UNKNOWN.DX07S024XJ1R1100 import {pad} as TestPad
class Footprint(Landpattern):
    p=TestPad().at(0,0)
class Schematic(Symbol):
    p=Pin((0,0),1,Direction.Right)
class Terminal(Component):
    p=Port()
    landpattern=Footprint()
    symbol=Schematic()
    mappings=[PadMapping({{p:landpattern.p}}),SymbolMapping({{p:symbol.p}})]
class TestCircuit(Circuit):
    p=Terminal().at(0,0)
class TestBoard(Board):
    shape=rectangle(10,10)
    signal_area=rectangle(10,10)
class FullBoardProxy(Design):
    circuit=TestCircuit()
    board=TestBoard()
    substrate=SubstratePcbgolf()
'''
(root/'runtime/original_proxy/design.py').write_text(source);(root/'source.py').write_text(source)

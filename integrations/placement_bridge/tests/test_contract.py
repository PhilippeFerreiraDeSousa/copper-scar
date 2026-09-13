"""Failure-mode checks against exported synthetic geometry, without live mutation."""
from pathlib import Path
import copy
import json
import sys
import tempfile
import unittest
import sexpdata as sx
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from contract import *
from copperhead import emit

FIXTURE=Path(__file__).parent/'fixtures'

class ContractTests(unittest.TestCase):
    def setUp(self):
        self.request=read(FIXTURE/'request.json');self.parent=FIXTURE/'02-parent';self.source=FIXTURE/'runtime-source.py'
    def validate(self):return validate_request(self.request,self.parent,self.source)
    def test_original_exact_identity(self):self.validate()
    def test_stale_parent(self):
        self.request['parent']['board_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'stale parent'):self.validate()
    def test_misassigned_pad(self):
        self.request['inventory']['refs']['TP4']['pads'][0]['net']='HOLD'
        with self.assertRaisesRegex(ValueError,'mapping'):self.validate()
    def test_missing_fixed_ref(self):
        self.request['fixed_refs'].remove('TP3')
        with self.assertRaisesRegex(ValueError,'fixed references'):self.validate()
    def test_wrong_coordinate_frame(self):
        self.request['frame']['native_transform']['reflect_y']=False
        with self.assertRaisesRegex(ValueError,'coordinate frame'):self.validate()
    def test_undeclared_move(self):
        self.request['target']['ref']='TP5'
        with self.assertRaisesRegex(ValueError,'target'):self.validate()
    def test_all_nets_really_connected(self):
        for s in ('02-parent','03-moved'):
            c=coverage(pcb(FIXTURE/s));self.assertTrue(all(v['realized'] for v in c.values()))
            self.assertEqual(sum(v['vias'] for v in c.values()),6)
    def test_removed_bottom_segment_exposes_open(self):
        b=sx.loads(pcb(self.parent).read_text());segment=next(s for s in children(b,'segment') if str(one(s,'layer')[1])=='B.Cu');b.remove(segment)
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'open.kicad_pcb';p.write_text(sx.dumps(b))
            self.assertEqual(sum(not n['realized'] for n in coverage(p).values()),1)
    def test_definition_does_not_connect_layers(self):
        b=sx.loads(pcb(self.parent).read_text());b[:]=[v for v in b if v not in children(b,'via')]
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'no-vias.kicad_pcb';p.write_text(sx.dumps(b))
            self.assertEqual(sum(not n['realized'] for n in coverage(p).values()),3)
    def test_uuid_churn_only(self):
        b=sx.loads(pcb(self.parent).read_text());one(children(b,'footprint')[0],'tstamp')[1]='new-export-id'
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'ids.kicad_pcb';p.write_text(sx.dumps(b))
            self.assertNotEqual(sha(p),sha(pcb(self.parent)));self.assertEqual(state_sha(p),state_sha(pcb(self.parent)))
            one(children(b,'segment')[0],'width')[1]=.19;p.write_text(sx.dumps(b))
            self.assertNotEqual(state_sha(p),state_sha(pcb(self.parent)))
    def test_top_level_order_is_not_geometry(self):
        b=sx.loads(pcb(self.parent).read_text());b[1:]=reversed(b[1:])
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'reordered.kicad_pcb';p.write_text(sx.dumps(b))
            self.assertEqual(state_sha(p),state_sha(pcb(self.parent)))
    def test_request_immutable(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'request.json';emit(self.parent,self.source,p)
            with self.assertRaises(FileExistsError):emit(self.parent,self.source,p)

if __name__=='__main__':unittest.main()

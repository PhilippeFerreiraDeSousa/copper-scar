"""Recorded native geometry and contract failure checks; no CAD mutation."""
from pathlib import Path
import copy
import gzip
import json
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qualify import GATES,layer,difference,trial_gate,verify_request
from shapely.geometry import Polygon

class QualificationTests(unittest.TestCase):
    def setUp(self):
        self.request={k:'a'*64 for k in ('parent_board_sha256','parent_project_sha256','inventory_sha256','boundaries_sha256')}
        self.observed=dict(self.request);self.gates={k:True for k in GATES}
    def test_matching_evidence_still_rejects_different_parent_state(self):
        self.gates['same_full_parent_state']=False
        self.assertFalse(trial_gate(self.request,self.observed,self.gates)['may_mutate'])
    def test_stale_parent(self):
        self.request['parent_board_sha256']='b'*64
        with self.assertRaisesRegex(ValueError,'stale parent'):verify_request(self.request,self.observed)
    def test_constraints_mismatch(self):
        self.request['parent_project_sha256']='b'*64
        with self.assertRaisesRegex(ValueError,'constraints mismatch'):verify_request(self.request,self.observed)
    def test_mapping_mismatch(self):
        self.request['inventory_sha256']='b'*64
        with self.assertRaisesRegex(ValueError,'mapping mismatch'):verify_request(self.request,self.observed)
    def test_dropped_external_terminal(self):
        self.request['boundaries_sha256']='b'*64
        with self.assertRaisesRegex(ValueError,'external boundary'):verify_request(self.request,self.observed)
    def test_omitted_gates_do_not_implicitly_pass(self):
        with self.assertRaisesRegex(ValueError,'incomplete'):trial_gate(self.request,self.observed,{})
    def test_proxy_does_not_require_generic_multilayer_planner(self):
        result=trial_gate(self.request,self.observed,self.gates)
        self.assertTrue(result['may_mutate']);self.assertFalse(result['generic_multilayer_planner_is_a_gate'])
    def test_measured_mask_correction_and_preserved_copper(self):
        with gzip.open(Path(__file__).parent/'mask-geometry.json.gz','rt') as f:r=json.load(f)
        a,b,c=[r[n] for n in ('copperhead','before','corrected')]
        before=difference(layer(a,'F.Mask'),layer(b,'F.Mask'))
        after=difference(layer(a,'F.Mask'),layer(c,'F.Mask'))
        self.assertGreater(before['hausdorff_mm'],.021)
        self.assertLess(after['hausdorff_mm'],.000063)
        self.assertFalse(after['exact_native_polygon_union'])
        for l in ('F.Cu','F.Paste'):self.assertTrue(layer(b,l).equals(layer(c,l)))
        self.assertEqual(b['pose'],c['pose'])
    def test_empty_absent_mask_is_not_nan(self):
        self.assertEqual(difference(Polygon(),Polygon())['hausdorff_mm'],0)

if __name__=='__main__':unittest.main()

import unittest
from feasibility import decide,ENGINEERING
class Admission(unittest.TestCase):
 def setUp(self):
  self.m=dict(incorrect_connections=0,missing_connections=10,physical_errors=2,physical_warnings=4,erc_errors=0,erc_warnings=0,parity_issues=0)
 def test_unknown_never_zero(self):
  for k in self.m:
   m=self.m.copy();m[k]=None;r=decide(m,True,True,{})
   self.assertIsNone(r['cost']);self.assertFalse(r['retain'])
 def test_failed_checker_never_retained(self):self.assertFalse(decide(self.m,True,False,{})['retain'])
 def test_topology_failure_never_retained(self):self.assertFalse(decide(self.m,False,True,{})['retain'])
 def test_regression_rejected(self):
  best=decide(self.m,True,True,{});m=self.m|{'missing_connections':1,'physical_errors':3};self.assertFalse(decide(m,True,True,{},best)['retain'])
 def test_improvement_retained_but_not_valid(self):
  best=decide(self.m,True,True,{});r=decide(self.m|{'missing_connections':9},True,True,{},best);self.assertTrue(r['retain']);self.assertFalse(r['valid']);self.assertIsNone(r['score'])
 def test_zero_without_engineering_is_not_valid(self):self.assertFalse(decide(dict.fromkeys(self.m,0),True,True,{})['valid'])
 def test_unverified_attestation_cannot_validate(self):
  e={k:{'passed':True,'artifact_sha256':'fixture','reviewer':'fixture'} for k in ENGINEERING};self.assertFalse(decide(dict.fromkeys(self.m,0),True,True,e)['valid'])
 def test_stage_two_needs_assembly(self):
  m=dict.fromkeys(self.m,0);e={k:{'passed':True,'verified':True,'artifact_sha256':'fixture','reviewer':'fixture'} for k in ENGINEERING};self.assertIsNone(decide(m,True,True,e,stage=2)['score']);self.assertEqual(decide(m,True,True,e,stage=2,volume=1000,vias=2,layers=2)['score'],11100)
if __name__=='__main__':unittest.main()

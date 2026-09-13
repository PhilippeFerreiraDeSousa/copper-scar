import tempfile,unittest
from pathlib import Path
from placement_parameters import render
class Placements(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.base=Path(self.tmp.name);self.src=self.base/'source.py';self.out=self.base/'result.py';self.src.write_text('class C:\n def __init__(self):\n  self.place(self.R1, Transform((1, 2)))\n  self.place(self.R2, Transform((3, 4)))\n')
 def test_empty_preserves_exact_initial_source(self):render(self.src,{},self.out);self.assertEqual(self.src.read_bytes(),self.out.read_bytes())
 def test_target_only_changes_and_survives_regeneration(self):
  p={'C.R1':{'x':9,'y':10,'angle':180}};r=render(self.src,p,self.out);self.assertEqual(r['changed_requests'],1);self.assertIn('self.place(self.R2, Transform((3, 4)))',self.out.read_text());first=self.out.read_bytes();render(self.src,p,self.out);self.assertEqual(first,self.out.read_bytes())
 def test_unknown_ref_rejected(self):
  with self.assertRaises(AssertionError):render(self.src,{'C.X':{'x':0,'y':0,'angle':0}},self.out)
 def test_nonfinite_rejected(self):
  with self.assertRaises(AssertionError):render(self.src,{'C.R1':{'x':float('nan'),'y':0,'angle':0}},self.out)
if __name__=='__main__':unittest.main()
